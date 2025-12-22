/**
 * Messages Page - Private messaging with datemates.
 */
import { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { messageService } from '../services/messageService';
import { datemateService } from '../services/datemateService';
import { aiService } from '../services/aiService';
import { reportUser } from '../services/reportService';
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
                    // Calculate partner ID
                    const partnerId = connection.requester_id === user?.id ? connection.receiver_id : connection.requester_id;

                    // Fetch partner profile explicitly since connection object lacks it
                    let fetchedProfile = {};
                    try {
                        fetchedProfile = await import('../services/profileService').then(m => m.profileService.getProfile(partnerId));
                    } catch (err) {
                        console.error("Failed to fetch partner profile", err);
                    }

                    setPartner({
                        id: partnerId,
                        display_name: fetchedProfile.display_name || `User ${partnerId}`,
                        bio: fetchedProfile.bio || "Datemate",
                        avatar_url: fetchedProfile.avatar_url,
                        interests: fetchedProfile.interests
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

    const handleReport = async () => {
        if (!partner) return;
        const reason = window.prompt("Why are you reporting this user?");
        if (reason) {
            try {
                const result = await reportUser({
                    reported_user_id: partner.id,
                    chat_type: "private",
                    partner_id: partner.id,
                    reason: reason
                });
                alert(result.message);
                if (result.action_taken === "deleted") {
                    // User deleted, navigate away
                    window.location.href = '/datemates';
                }
            } catch (error) {
                alert("Failed to report user: " + (error.response?.data?.detail || error.message));
            }
        }
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
            <div className="chat-wrapper">
                <div className="chat-header">
                    <div className="chat-header-info">
                        {partner?.display_name ? (
                            <div className="chat-partner-avatar-placeholder">
                                {partner.display_name[0].toUpperCase()}
                            </div>
                        ) : (
                            <div className="chat-partner-avatar-placeholder">?</div>
                        )}
                        <div className="chat-partner-details">
                            <div className="partner-name-row">
                                <h3>{partner?.display_name || 'Datemate'}</h3>
                                {partner && (partner.age || partner.gender) && (
                                    <span className="partner-demographics">
                                        {partner.age && `${partner.age} y/o`}
                                        {partner.gender && (partner.gender === 'Male' ? ' ♂' : partner.gender === 'Female' ? ' ♀' : '')}
                                    </span>
                                )}
                            </div>
                            {partner?.bio && <p className="partner-bio" title={partner.bio}>{partner.bio}</p>}
                        </div>
                    </div>
                    <div className="chat-header-actions" style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                        {partner?.interests && partner.interests.length > 0 && (
                            <div className="partner-tags-mini" style={{ marginTop: 0 }}>
                                {partner.interests.slice(0, 3).map((tag, i) => (
                                    <span key={i} className="mini-tag">{tag}</span>
                                ))}
                            </div>
                        )}
                        <button
                            className="btn btn-sm btn-danger"
                            style={{ backgroundColor: '#dc3545', color: 'white', border: 'none', padding: '5px 10px', borderRadius: '4px', cursor: 'pointer' }}
                            onClick={handleReport}
                        >
                            Report
                        </button>
                    </div>
                </div>

                <div className="messages-container">
                    {messages.map(msg => (
                        <div key={msg.id} className={`message ${msg.sender}`}>
                            <div className="message-bubble">
                                {msg.text}
                            </div>
                            <div className="message-time">
                                {new Date(msg.createdAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                            </div>
                        </div>
                    ))}
                    <div ref={messagesEndRef} />
                </div>

                <form onSubmit={handleSend} className="message-input-area">
                    <input
                        type="text"
                        className="message-input"
                        value={inputText}
                        onChange={(e) => setInputText(e.target.value)}
                        placeholder="Type a message..."
                    />
                    <button
                        type="button"
                        className="btn btn-ghost"
                        onClick={openWingman}
                        title="Wingman Help"
                        style={{ marginRight: '5px', fontSize: '1.2rem', padding: '0 10px' }}
                    >
                        💡
                    </button>
                    <button
                        type="button"
                        className="btn btn-ghost"
                        onClick={handleOpenMissEx}
                        title="Miss Ex"
                        style={{ marginRight: '5px', fontSize: '1.2rem', padding: '0 10px' }}
                    >
                        💔
                    </button>
                    <button type="submit" className="send-btn">
                        ➤
                    </button>
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
                title={`💔${partner?.display_name}.copy`}
            />
        </div>
    );
}

export default MessagesPage;
