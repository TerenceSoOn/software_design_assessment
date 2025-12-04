/**
 * AI Companion Page
 * Hub for all AI features: Companion Chat, Practice Mode, Profile Optimizer
 */
import { useState, useEffect, useRef } from 'react';
import { aiService } from '../services/aiService';
import { useAuth } from '../context/AuthContext';
import './AICompanionPage.css';

function AICompanionPage() {
    const [activeTab, setActiveTab] = useState('companion'); // companion, practice, optimizer
    const [messages, setMessages] = useState([]);
    const [inputText, setInputText] = useState('');
    const [loading, setLoading] = useState(false);
    const [profileTips, setProfileTips] = useState('');
    const messagesEndRef = useRef(null);
    const { user } = useAuth();

    // Initial greeting based on tab
    useEffect(() => {
        setMessages([]);
        if (activeTab === 'companion') {
            setMessages([{
                role: 'assistant',
                content: `Hi ${user?.username || 'there'}! I'm your AI Companion. I'm here to chat, listen, or just keep you company. How are you feeling today?`
            }]);
        } else if (activeTab === 'practice') {
            setMessages([{
                role: 'assistant',
                content: "Hi! I'm ready to practice chatting with you. Pretend I'm a match you just connected with. You can start by saying hello!"
            }]);
        }
    }, [activeTab, user]);

    // Auto-scroll
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const handleSend = async (e) => {
        e.preventDefault();
        if (!inputText.trim() || loading) return;

        const userMsg = { role: 'user', content: inputText };
        setMessages(prev => [...prev, userMsg]);
        setInputText('');
        setLoading(true);

        try {
            let response;
            if (activeTab === 'companion') {
                // Send history for context
                const history = messages.map(m => ({ role: m.role, content: m.content }));
                const res = await aiService.chatCompanion(userMsg.content, history);
                response = res.response;
            } else if (activeTab === 'practice') {
                const history = messages.map(m => ({ role: m.role, content: m.content }));
                const res = await aiService.practiceChat(userMsg.content, history);
                response = res.response;
            }

            setMessages(prev => [...prev, { role: 'assistant', content: response }]);
        } catch (err) {
            setMessages(prev => [...prev, {
                role: 'system',
                content: 'Sorry, I encountered an error. Please try again.'
            }]);
        } finally {
            setLoading(false);
        }
    };

    const handleOptimizeProfile = async () => {
        if (!user?.profile?.bio && !user?.profile?.interests) {
            setProfileTips("Please add a bio or interests to your profile first so I can analyze it!");
            return;
        }

        setLoading(true);
        try {
            const profileText = `
                Display Name: ${user.username}
                Bio: ${user.profile?.bio || 'Not set'}
                Interests: ${user.profile?.interests?.join(', ') || 'None'}
                Age: ${user.profile?.age || 'Not set'}
            `;
            const res = await aiService.optimizeProfile(profileText);
            setProfileTips(res.tips);
        } catch (err) {
            setProfileTips("Failed to analyze profile. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container ai-page">
            <div className="ai-container card">
                <div className="ai-header">
                    <h1>AI Features</h1>
                    <div className="ai-tabs">
                        <button
                            className={`tab-btn ${activeTab === 'companion' ? 'active' : ''}`}
                            onClick={() => setActiveTab('companion')}
                        >
                            AI Companion
                        </button>
                        <button
                            className={`tab-btn ${activeTab === 'practice' ? 'active' : ''}`}
                            onClick={() => setActiveTab('practice')}
                        >
                            Practice Mode
                        </button>
                        <button
                            className={`tab-btn ${activeTab === 'optimizer' ? 'active' : ''}`}
                            onClick={() => setActiveTab('optimizer')}
                        >
                            Profile Optimizer
                        </button>
                    </div>
                </div>

                <div className="ai-content">
                    {activeTab === 'optimizer' ? (
                        <div className="optimizer-section">
                            <h3>Profile Analysis</h3>
                            <p>Get AI-powered tips to improve your profile and get more matches.</p>

                            <button
                                className="btn btn-primary"
                                onClick={handleOptimizeProfile}
                                disabled={loading}
                            >
                                {loading ? 'Analyzing...' : 'Analyze My Profile'}
                            </button>

                            {profileTips && (
                                <div className="tips-result">
                                    <h4>Suggestions:</h4>
                                    <div className="tips-content">
                                        {profileTips.split('\n').map((tip, i) => (
                                            <p key={i}>{tip}</p>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    ) : (
                        // Chat Interface for Companion and Practice
                        <div className="ai-chat-interface">
                            <div className="messages-area">
                                {messages.map((msg, idx) => (
                                    <div key={idx} className={`message ${msg.role === 'user' ? 'me' : 'partner'}`}>
                                        <div className="message-bubble">
                                            {msg.content}
                                        </div>
                                    </div>
                                ))}
                                {loading && (
                                    <div className="message partner">
                                        <div className="message-bubble typing">
                                            <span>.</span><span>.</span><span>.</span>
                                        </div>
                                    </div>
                                )}
                                <div ref={messagesEndRef} />
                            </div>

                            <form onSubmit={handleSend} className="chat-input-area">
                                <input
                                    type="text"
                                    className="input chat-input"
                                    placeholder="Type a message..."
                                    value={inputText}
                                    onChange={(e) => setInputText(e.target.value)}
                                    disabled={loading}
                                />
                                <button type="submit" className="btn btn-primary" disabled={loading}>
                                    Send
                                </button>
                            </form>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default AICompanionPage;
