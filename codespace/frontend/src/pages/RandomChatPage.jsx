/**
 * Random Chat Page - Real-time chat with random users.
 */
import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { io } from 'socket.io-client';
import { useAuth } from '../context/AuthContext';
import { datemateService } from '../services/datemateService';
import { aiService } from '../services/aiService';
import AIChatModal from '../components/ai/AIChatModal';
import WingmanModal from '../components/ai/WingmanModal';
import './RandomChatPage.css';

function RandomChatPage() {
    const [socket, setSocket] = useState(null);
    const [messages, setMessages] = useState([]);
    const [inputText, setInputText] = useState('');
    const [status, setStatus] = useState('connecting'); // connecting, searching, matched, disconnected
    const [partner, setPartner] = useState(null);
    const [showConnectionRequest, setShowConnectionRequest] = useState(false);
    const messagesEndRef = useRef(null);
    const { user, profile, token } = useAuth();
    const navigate = useNavigate();

    // AI Features State
    const [atmosphere, setAtmosphere] = useState(null);
    const [showAIChat, setShowAIChat] = useState(false);
    const [aiChatHistory, setAiChatHistory] = useState([]);
    const [aiInputText, setAiInputText] = useState('');
    const aiMessagesEndRef = useRef(null);

    // Wingman (Help) State
    const [showWingman, setShowWingman] = useState(false);
    const [wingmanSuggestions, setWingmanSuggestions] = useState([]);
    const [wingmanAtmosphere, setWingmanAtmosphere] = useState(null);
    const [loadingWingman, setLoadingWingman] = useState(false);

    // Connection Status State
    const [connectionStatus, setConnectionStatus] = useState({ isConnected: false, isPending: false, status: 'none' });

    // Initialize Socket.IO connection
    useEffect(() => {
        if (!token) return; // Wait for token

        // Use the API URL from environment variables (which now points to LAN IP)
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

        const newSocket = io(apiUrl, {
            path: '/socket.io/',
            transports: ['websocket', 'polling'],
            reconnection: true,
            reconnectionDelay: 1000,
            reconnectionAttempts: 5,
            auth: { token } // Pass token for authentication
        });

        setSocket(newSocket);

        newSocket.on('connect', () => {
            console.log('Connected to socket server');
            setStatus('searching');
            // Join queue immediately upon connection
            newSocket.emit('join_queue', {
                token,
                gender: profile?.gender,
                preferred_gender: profile?.preferred_gender,
                profile: {
                    display_name: profile?.display_name || user?.username,
                    age: profile?.age,
                    interests: profile?.interests,
                    bio: profile?.bio,
                    gender: profile?.gender,
                    avatar_url: profile?.avatar_url
                }
            });
        });

        newSocket.on('match_found', (data) => {
            setStatus('matched');
            setPartner(data.partner);
            setMessages([{
                id: Date.now(),
                sender: 'system',
                text: `You are connected with ${data.partner.display_name || 'a random stranger'}. Say hi!`
            }]);

            // Check connection status immediately
            if (data.partner && data.partner.user_id) {
                datemateService.checkConnectionStatus(data.partner.user_id)
                    .then(status => setConnectionStatus(status))
                    .catch(err => console.error("Failed to check status", err));
            }
        });

        newSocket.on('receive_message', (data) => {
            setMessages(prev => [...prev, {
                id: Date.now(),
                sender: 'partner',
                text: data.message,
                timestamp: data.timestamp
            }]);
        });

        newSocket.on('partner_disconnected', () => {
            setStatus('disconnected');
            setMessages(prev => [...prev, {
                id: Date.now(),
                sender: 'system',
                text: 'Partner has disconnected.'
            }]);
            setShowConnectionRequest(true);
        });

        newSocket.on('partner_left', () => {
            setStatus('disconnected');
            setMessages(prev => [...prev, {
                id: Date.now(),
                sender: 'system',
                text: 'Partner has left the chat.'
            }]);
            setShowConnectionRequest(true);
        });

        newSocket.on('datemate_request_received', (data) => {
            setMessages(prev => [...prev, {
                id: Date.now(),
                sender: 'system',
                text: `Partner wants to be datemates! "${data.message}"`
            }]);
            // Update status nicely
            setConnectionStatus(prev => ({ ...prev, isPending: true, status: 'pending_incoming' }));
        });

        newSocket.on('error', (data) => {
            console.error('Socket error:', data);
            setMessages(prev => [...prev, {
                id: Date.now(),
                sender: 'system',
                text: `Error: ${data.message}`
            }]);
        });

        return () => {
            newSocket.disconnect();
        };
    }, [token, user]);

    // Auto-scroll to bottom
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // Auto-scroll AI chat
    useEffect(() => {
        aiMessagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [aiChatHistory]);

    // Atmosphere Analyzer (runs every 5 messages)
    useEffect(() => {
        if (status === 'matched' && messages.length > 0 && messages.length % 5 === 0) {
            const history = messages
                .filter(m => m.sender === 'me' || m.sender === 'partner')
                .map(m => ({
                    role: m.sender === 'me' ? 'User' : 'Partner',
                    content: m.text
                }));

            aiService.analyzeAtmosphere(history)
                .then(data => {
                    if (data.analysis) {
                        try {
                            // Try to parse JSON if the AI returned JSON string
                            const analysis = JSON.parse(data.analysis);
                            setAtmosphere(analysis);
                        } catch (e) {
                            // Fallback if plain text
                            setAtmosphere({ feedback: data.analysis });
                        }
                    }
                })
                .catch(err => console.error('Atmosphere analysis failed:', err));
        }
    }, [messages, status]);

    const handleSend = async (e) => {
        e.preventDefault();
        if (!inputText.trim() || status !== 'matched') return;

        const messageText = inputText;
        setInputText('');

        // Optimistic UI update
        setMessages(prev => [...prev, {
            id: Date.now(),
            sender: 'me',
            text: messageText
        }]);

        // Check safety (AI feature)
        try {
            const safetyCheck = await aiService.checkSafety(messageText);
            if (!safetyCheck.is_safe) {
                setMessages(prev => [...prev, {
                    id: Date.now() + 1,
                    sender: 'system',
                    text: `⚠️ Warning: Your message was flagged as potentially unsafe (${safetyCheck.reason}). Please be respectful.`
                }]);
                // Don't send if unsafe? Or just warn? For now, we warn but send (or could block)
                // If strictly blocking: return; 
            }
        } catch (err) {
            console.error('Safety check failed', err);
        }

        // Send to server
        socket.emit('send_message', {
            message: messageText,
            timestamp: new Date().toISOString()
        });
    };

    const handleLeave = () => {
        if (socket) {
            socket.emit('leave_chat');
            socket.disconnect();
        }
        setStatus('disconnected');
        setShowConnectionRequest(true);
    };

    const sendDatemateRequest = async () => {
        if (!partner) return;
        try {
            // Send via API (persistent)
            await datemateService.sendRequest(partner.user_id);

            // Also notify via socket for real-time feedback
            socket.emit('send_datemate_request', { message: "Let's be datemates!" });

            alert('Datemate request sent!');
            setConnectionStatus({ isConnected: false, isPending: true, status: 'pending_outgoing' });
            // Don't navigate away, let them chat more if they want? Or maybe navigate home
            // navigate('/');
        } catch (error) {
            alert('Failed to send request: ' + (error.response?.data?.detail || error.message));
        }
    };

    const handleAIChatSend = async (e) => {
        e.preventDefault();
        if (!aiInputText.trim()) return;

        const text = aiInputText;
        setAiInputText('');

        // Add user message
        const newHistory = [...aiChatHistory, { role: 'user', content: text }];
        setAiChatHistory(newHistory);

        try {
            // Get AI response
            const response = await aiService.chatWithCompanion(text, aiChatHistory);
            setAiChatHistory([...newHistory, { role: 'assistant', content: response.reply || response }]); // Adjust based on actual response structure
        } catch (error) {
            console.error('AI Chat error:', error);
            setAiChatHistory([...newHistory, { role: 'assistant', content: "I'm having trouble connecting right now." }]);
        }
    };

    const toggleAIChat = () => {
        setShowAIChat(!showAIChat);
        if (!showAIChat && aiChatHistory.length === 0) {
            // Initial greeting
            setAiChatHistory([{ role: 'assistant', content: "Hi! I'm your AI Companion. Waiting can be boring, so I'm here to chat! How are you doing?" }]);
        }
    };

    const openWingman = async () => {
        if (!partner) return;
        setLoadingWingman(true);
        setShowWingman(true);
        setWingmanSuggestions([]);
        setWingmanAtmosphere(null);

        try {
            // Build chat history
            const chatHistory = messages
                .filter(m => m.sender === 'me' || m.sender === 'partner')
                .map(m => ({ role: m.sender === 'me' ? 'user' : 'assistant', content: m.text }));

            // Get Wingman analysis and suggestions (now returns { analysis, suggestions })
            const wingmanResult = await aiService.getWingmanSuggestions({
                display_name: partner.display_name,
                interests: partner.interests,
                bio: partner.bio
            }, chatHistory);

            setWingmanAtmosphere(wingmanResult.analysis || "Analyzing the situation...");
            setWingmanSuggestions(wingmanResult.suggestions || []);

        } catch (error) {
            console.error("Wingman failed", error);
            setWingmanSuggestions(["Be casual and friendly!", "Ask about their interests!", "Share something fun about yourself!"]);
            setWingmanAtmosphere("Could not analyze the conversation.");
        } finally {
            setLoadingWingman(false);
        }
    };

    const handleWingmanSelect = (suggestion) => {
        setInputText(suggestion);
        setShowWingman(false);
    };

    const renderDatemateButton = () => {
        if (connectionStatus.isConnected) {
            return <button className="btn btn-outline" disabled>You are datemates</button>;
        }
        if (connectionStatus.status === 'pending_outgoing') {
            return <button className="btn btn-outline" disabled>Request Sent</button>;
        }
        if (connectionStatus.status === 'pending_incoming') {
            return <button className="btn btn-primary" onClick={() => navigate('/datemates')}>Accept Request</button>; // Redirect to accept
        }
        return (
            <button
                className="btn btn-primary"
                onClick={sendDatemateRequest}
            >
                Send Datemate Request
            </button>
        );
    };

    return (
        <div className="random-chat-page">
            <AIChatModal
                isOpen={showAIChat}
                onClose={() => setShowAIChat(false)}
                history={aiChatHistory}
                onSend={handleAIChatSend}
                inputText={aiInputText}
                setInputText={setAiInputText}
                messagesEndRef={aiMessagesEndRef}
                title="🤖 AI Companion"
            />

            <WingmanModal
                isOpen={showWingman}
                onClose={() => setShowWingman(false)}
                atmosphere={wingmanAtmosphere}
                suggestions={wingmanSuggestions}
                onSelectSuggestion={handleWingmanSelect}
            />

            <div className="chat-container">
                {/* Chat Header */}
                <div className="chat-header">
                    <div className="header-left">
                        <div className="partner-info">
                            {status === 'matched' && partner ? (
                                <>
                                    <div className="partner-avatar-container">
                                        {partner.avatar_url ? (
                                            <img src={partner.avatar_url} alt="Partner" className="partner-avatar-img" />
                                        ) : (
                                            <div className="partner-avatar-placeholder">
                                                {partner.display_name?.[0]?.toUpperCase() || '?'}
                                            </div>
                                        )}
                                        <span className={`status-indicator ${status === 'matched' ? 'online' : ''}`}></span>
                                    </div>
                                    <div className="partner-text">
                                        <h3>{partner.display_name || 'Random Stranger'}</h3>
                                        {partner.bio && <p className="partner-bio">{partner.bio.slice(0, 50)}...</p>}
                                    </div>
                                </>
                            ) : (
                                <div className="partner-text">
                                    <h3>{status === 'searching' ? '🔍 Searching for a match...' : 'Disconnected'}</h3>
                                </div>
                            )}
                        </div>
                    </div>
                    <div className="header-right">
                        {status === 'matched' && partner?.interests && partner.interests.length > 0 && (
                            <div className="partner-tags">
                                {partner.interests.slice(0, 3).map((tag, i) => (
                                    <span key={i} className="interest-tag">{tag}</span>
                                ))}
                            </div>
                        )}
                        <button className="leave-btn" onClick={handleLeave}>
                            Leave Chat
                        </button>
                    </div>
                </div>

                {/* Messages Area */}
                <div className="messages-area">
                    {messages.map(msg => (
                        <div key={msg.id} className={`message ${msg.sender}`}>
                            <div className="message-bubble">
                                {msg.text}
                            </div>
                        </div>
                    ))}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area or Status */}
                {status === 'matched' ? (
                    <form onSubmit={handleSend} className="chat-input-area">
                        <button
                            type="button"
                            className="help-btn"
                            onClick={openWingman}
                            title="Get help from AI Wingman"
                        >
                            💡 Help
                        </button>
                        <input
                            type="text"
                            className="chat-input"
                            placeholder="Type your message..."
                            value={inputText}
                            onChange={(e) => setInputText(e.target.value)}
                        />
                        <button type="submit" className="send-btn">
                            <span>➤</span>
                        </button>
                    </form>
                ) : (
                    <div className="status-area">
                        {status === 'searching' ? (
                            <div className="searching-container">
                                <div className="loader"></div>
                                <p>Looking for someone compatible...</p>
                                <button className="btn btn-outline" onClick={toggleAIChat}>
                                    🤖 Chat with AI while waiting
                                </button>
                            </div>
                        ) : (
                            <div className="ended-container">
                                <p className="ended-text">Chat ended</p>
                                {partner && (
                                    <div className="ended-actions">
                                        <p>Enjoyed chatting with {partner.display_name}?</p>
                                        {renderDatemateButton()}
                                    </div>
                                )}
                                <div className="nav-buttons">
                                    <button className="btn btn-primary" onClick={() => window.location.reload()}>
                                        New Random Chat
                                    </button>
                                    <button className="btn btn-secondary" onClick={() => navigate('/')}>
                                        Return Home
                                    </button>
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}

export default RandomChatPage;
