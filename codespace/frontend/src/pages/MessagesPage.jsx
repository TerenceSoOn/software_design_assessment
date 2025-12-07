/**
 * Messages Page - Private messaging with datemates.
 */
import { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { messageService } from '../services/messageService';
import { datemateService } from '../services/datemateService';
import { aiService } from '../services/aiService';
import { useAuth } from '../context/AuthContext';
import AIChatModal from '../components/ai/AIChatModal';
import WingmanModal from '../components/ai/WingmanModal';
import './MessagesPage.css';

function MessagesPage() {
    const { connectionId } = useParams();
    const { user, profile } = useAuth();
    const [messages, setMessages] = useState([]);
    const [inputText, setInputText] = useState('');
    const [partner, setPartner] = useState(null);
    const [loading, setLoading] = useState(true);
    const messagesEndRef = useRef(null);

    // Miss Ex modal state
    const [showMissEx, setShowMissEx] = useState(false);
    const [missExHistory, setMissExHistory] = useState([]);
    const [missExInput, setMissExInput] = useState('');
    const missExEndRef = useRef(null);

    useEffect(() => {
        const loadData = async () => {
            if (!connectionId) return;
            try {
                // 1. Fetch datemate details to get partner info
                const datemates = await datemateService.getDatemates();
                // connectionId might be the connection ID or the user ID. 
                // The URL usually passes the ID of the resource. 
                // Let's assume connectionId is the PARTNER'S USER ID for simplicity in this flow, 
                // or we need to find the connection that matches.
                // However, the router link in DatematesPage says `navigate(/messages/${datemateId})` where datemateId is connection.id

                // Let's find the connection by ID
                const connection = datemates.find(d => d.id === parseInt(connectionId));

                if (connection) {
                    // We need the partner's user ID to fetch messages
                    // The connection object has requester_id and receiver_id. 
                    // We need to figure out which one is the partner.
                    // Since we don't have 'user' in context yet, we need to get it.
                    // Assuming 'user' is available from useAuth()

                    // Actually, the backend endpoint `GET /messages/{user_id}` expects the PARTNER'S USER ID.
                    // But we have the CONNECTION ID from the URL.
                    // We need to derive the partner's user ID from the connection object.
                    // The connection object from `getDatemates` (which calls `/connections`) returns:
                    // { id, requester_id, receiver_id, status, ... }
                    // We need to know our own ID to pick the other one.

                    // Ideally, we should pass the partner's user ID in the URL, e.g. /messages/user/123
                    // But if we stick to connection ID, we need logic here.

                    // Let's assume for now we can get the partner ID. 
                    // If `user` is not loaded yet, we might have issues.
                    // Let's fetch messages using the connection's partner ID.

                    const partnerId = connection.requester_id === user?.id ? connection.receiver_id : connection.requester_id;

                    // Mock partner profile for now since connection doesn't have full profile
                    // In a real app, we'd fetch profile by ID.
                    setPartner({
                        id: partnerId,
                        display_name: `User ${partnerId}`, // Placeholder
                        bio: "Datemate"
                    });

                    // 2. Fetch messages
                    const msgs = await messageService.getConversation(partnerId);
                    setMessages(msgs.map(m => ({
                        id: m.id,
                        sender: m.sender_id === user?.id ? 'me' : 'partner',
                        text: m.content,
                        createdAt: m.created_at
                    })));
                } else {
                    // Fallback or error
                    console.error("Connection not found");
                }

            } catch (error) {
                console.error("Failed to load chat data", error);
            } finally {
                setLoading(false);
            }
        };

        if (user) {
            loadData();
        }
    }, [connectionId, user]);

    // Auto-scroll to bottom when messages change
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // Open Miss Ex modal
    const handleOpenMissEx = () => {
        setMissExHistory([
            { role: 'system', content: `You are imitating ${partner?.display_name || 'your ex'}. Respond in their style and personality.` }
        ]);
        setShowMissEx(true);
    };

    // Poll for new messages every 3 seconds
    useEffect(() => {
        if (!partner) return;

        const pollMessages = async () => {
            try {
                const conversation = await messageService.getConversation(partner.id);
                // Only update if we have new messages (simple length check or last ID check could be better, but complete replace is safer for sync)
                // For now, replacing is fine as React handles diffing
                const formattedMessages = conversation.map(msg => ({
                    id: msg.id,
                    sender: msg.sender_id === partner.id ? 'them' : 'me',
                    text: msg.content,
                    createdAt: msg.created_at
                }));
                setMessages(formattedMessages);
            } catch (error) {
                console.error("Failed to poll messages", error);
            }
        };

        const intervalId = setInterval(pollMessages, 3000);
        return () => clearInterval(intervalId);
    }, [partner]); // Re-run when partner changes

    // Handle Miss Ex modal chat
    const handleMissExSend = async (message) => {
        if (!message.trim()) return;

        const newHistory = [...missExHistory, { role: 'user', content: message }];
        setMissExHistory(newHistory);
        setMissExInput('');

        try {
            const history = messages.map(m => ({
                role: m.sender === 'me' ? 'user' : 'assistant',
                content: m.text
            }));
            const partnerProfileStr = `Name: ${partner?.display_name || 'Partner'}, Bio: ${partner?.bio || 'Unknown'}`;

            // Pass partner.id as the targetUserId
            const response = await aiService.imitateEx(message, history, '', partner.id);
            // Verify structure: backend likely returns { response: "..." }
            // If aiService returns response.data directly, then 'response' IS the data object.
            const aiReply = response.response || response;

            setMissExHistory(prev => [...prev, { role: 'assistant', content: aiReply }]);
        } catch (error) {
            console.error("Miss Ex failed:", error);
            setMissExHistory(prev => [...prev, { role: 'assistant', content: "Sorry, I couldn't respond. Please try again." }]);
        }
    };

    // Wingman (Help) State for Messages
    const [showWingman, setShowWingman] = useState(false);
    const [wingmanSuggestions, setWingmanSuggestions] = useState([]);
    const [wingmanAtmosphere, setWingmanAtmosphere] = useState(null);

    const openWingman = async () => {
        if (!partner) return;
        setShowWingman(true);
        setWingmanSuggestions([]);
        setWingmanAtmosphere(null);

        try {
            // Build chat history
            const chatHistory = messages.map(m => ({
                role: m.sender === 'me' ? 'user' : 'assistant',
                content: m.text
            }));

            // Get Wingman analysis and suggestions (now returns { analysis, suggestions })
            const wingmanResult = await aiService.getWingmanSuggestions({
                display_name: partner.display_name,
                interests: partner.interests || [],
                bio: partner.bio || ''
            }, chatHistory);

            setWingmanAtmosphere(wingmanResult.analysis || "Analyzing the situation...");
            setWingmanSuggestions(wingmanResult.suggestions || []);

        } catch (error) {
            console.error("Wingman failed", error);
            setWingmanSuggestions(["Be casual and friendly!", "Ask about their interests!", "Share something fun about yourself!"]);
            setWingmanAtmosphere("Could not analyze the conversation.");
        }
    };

    const handleWingmanSelect = (suggestion) => {
        setInputText(suggestion);
        setShowWingman(false);
    };

    const handleSend = async (e) => {
        e.preventDefault();
        if (!inputText.trim() || !partner) return;

        try {
            const sentMsg = await messageService.sendMessage(partner.id, inputText);

            const newMsg = {
                id: sentMsg.id,
                sender: 'me',
                text: sentMsg.content,
                createdAt: sentMsg.created_at
            };
            setMessages([...messages, newMsg]);
            setInputText('');
        } catch (error) {
            console.error("Failed to send message", error);
            alert("Failed to send message");
        }
    };

    if (!connectionId) {
        return (
            <div className="container">
                <div className="card text-center">
                    <h3>Select a datemate to start messaging</h3>
                </div>
            </div>
        );
    }

    return (
        <div className="container messages-page">
            <div className="messages-card card">
                <div className="messages-header">
                    <h3>Datemate Chat</h3>
                </div>

                <div className="messages-list">
                    {messages.map(msg => (
                        <div key={msg.id} className={`msg-row ${msg.sender}`}>
                            <div className="msg-bubble">
                                {msg.text}
                            </div>
                        </div>
                    ))}
                    <div ref={messagesEndRef} />
                </div>

                <form onSubmit={handleSend} className="msg-input-area">
                    <input
                        type="text"
                        className="input"
                        value={inputText}
                        onChange={(e) => setInputText(e.target.value)}
                        placeholder="Type a message..."
                    />
                    <button
                        type="button"
                        className="btn btn-ghost"
                        onClick={openWingman}
                        title="How to respond to this?"
                        style={{ marginRight: '5px', fontSize: '1rem' }}
                    >
                        💡 Help
                    </button>
                    <button
                        type="button"
                        className="btn btn-ghost"
                        onClick={handleOpenMissEx}
                        title="I miss this one so much"
                        style={{ marginRight: '10px', fontSize: '1.2rem' }}
                    >
                        💔 Miss
                    </button>
                    <button type="submit" className="btn btn-primary">Send</button>
                </form>
            </div>

            <WingmanModal
                isOpen={showWingman}
                onClose={() => setShowWingman(false)}
                atmosphere={wingmanAtmosphere}
                suggestions={wingmanSuggestions}
                onSelectSuggestion={handleWingmanSelect}
            />

            <AIChatModal
                isOpen={showMissEx}
                onClose={() => setShowMissEx(false)}
                history={missExHistory.filter(m => m.role !== 'system')}
                onSend={handleMissExSend}
                inputText={missExInput}
                setInputText={setMissExInput}
                messagesEndRef={missExEndRef}
                title={`💔 Reminiscing ${partner?.display_name || 'your ex'}...`}
            />
        </div>
    );
}

export default MessagesPage;
