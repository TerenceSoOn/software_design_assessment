/**
 * Random Chat Page - Real-time chat with random users.
 */
import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { io } from 'socket.io-client';
import { useAuth } from '../context/AuthContext';
import { connectionService } from '../services/connectionService';
import { aiService } from '../services/aiService';
import './RandomChatPage.css';

function RandomChatPage() {
    const [socket, setSocket] = useState(null);
    const [messages, setMessages] = useState([]);
    const [inputText, setInputText] = useState('');
    const [status, setStatus] = useState('connecting'); // connecting, searching, matched, disconnected
    const [partner, setPartner] = useState(null);
    const [showConnectionRequest, setShowConnectionRequest] = useState(false);
    const messagesEndRef = useRef(null);
    const { user, token } = useAuth();
    const navigate = useNavigate();

    // Initialize Socket.IO connection
    useEffect(() => {
        const newSocket = io('http://localhost:8000', {
            auth: { token }
        });

        setSocket(newSocket);

        newSocket.on('connect', () => {
            console.log('Connected to socket server');
            setStatus('searching');
            // Join queue immediately upon connection
            newSocket.emit('join_queue', {
                token,
                gender: user?.gender,
                preferred_gender: user?.preferred_gender,
                profile: {
                    display_name: user?.username, // Fallback if profile not loaded
                    age: user?.profile?.age,
                    interests: user?.profile?.interests
                }
            });
        });

        newSocket.on('searching', (data) => {
            setStatus('searching');
            setMessages([{
                id: Date.now(),
                sender: 'system',
                text: data.message || 'Searching for a compatible partner...'
            }]);
        });

        newSocket.on('match_found', (data) => {
            setStatus('matched');
            setPartner(data.partner);
            setMessages([{
                id: Date.now(),
                sender: 'system',
                text: `You are connected with ${data.partner.display_name || 'a random stranger'}. Say hi!`
            }]);
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
            // Could add UI to accept/decline here
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
            await connectionService.sendRequest(partner.user_id);

            // Also notify via socket for real-time feedback
            socket.emit('send_datemate_request', { message: "Let's be datemates!" });

            alert('Datemate request sent!');
            navigate('/');
        } catch (error) {
            alert('Failed to send request: ' + (error.response?.data?.detail || error.message));
        }
    };

    return (
        <div className="container chat-page">
            <div className="chat-container card">
                <div className="chat-header">
                    <div className="partner-info">
                        <div className={`status-dot ${status === 'matched' ? 'online' : 'offline'}`}></div>
                        <h3>
                            {status === 'searching' ? 'Searching...' :
                                status === 'matched' ? (partner?.display_name || 'Random Stranger') :
                                    'Disconnected'}
                        </h3>
                        {status === 'matched' && partner?.interests && (
                            <span className="partner-interests">
                                Likes: {partner.interests.join(', ')}
                            </span>
                        )}
                    </div>
                    <button className="btn btn-secondary btn-sm" onClick={handleLeave}>
                        Leave Chat
                    </button>
                </div>

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

                {status === 'matched' ? (
                    <form onSubmit={handleSend} className="chat-input-area">
                        <button
                            type="button"
                            className="btn btn-secondary btn-icon"
                            onClick={async () => {
                                if (!partner) return;
                                const suggestions = await aiService.getWingmanSuggestions({
                                    display_name: partner.display_name,
                                    interests: partner.interests,
                                    bio: partner.bio
                                });
                                setInputText(suggestions[0] || '');
                            }}
                            title="AI Wingman Suggestions"
                        >
                            🤖
                        </button>
                        <input
                            type="text"
                            className="input chat-input"
                            placeholder="Type a message..."
                            value={inputText}
                            onChange={(e) => setInputText(e.target.value)}
                        />
                        <button type="submit" className="btn btn-primary">Send</button>
                    </form>
                ) : (
                    <div className="chat-ended-actions">
                        {status === 'searching' ? (
                            <div className="searching-animation">
                                <p>Looking for someone compatible...</p>
                                <div className="loader"></div>
                            </div>
                        ) : (
                            <>
                                <p>Chat ended.</p>
                                {showConnectionRequest && partner && (
                                    <div className="connection-prompt">
                                        <p>Did you enjoy the chat with {partner.display_name}?</p>
                                        <button
                                            className="btn btn-primary"
                                            onClick={sendDatemateRequest}
                                        >
                                            Send Datemate Request
                                        </button>
                                        <button
                                            className="btn btn-secondary"
                                            onClick={() => navigate('/')}
                                        >
                                            Return Home
                                        </button>
                                    </div>
                                )}
                            </>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}

export default RandomChatPage;
