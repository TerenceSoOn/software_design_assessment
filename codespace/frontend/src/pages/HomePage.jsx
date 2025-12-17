/**
 * Home Page - Landing page and Random Chat entry point.
 */
import { useState, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { aiService } from '../services/aiService';
import AIChatModal from '../components/ai/AIChatModal';
import './HomePage.css';

function HomePage() {
    const { user } = useAuth();
    const navigate = useNavigate();

    // Practice Mode State
    const [showPracticeMode, setShowPracticeMode] = useState(false);
    const [practiceHistory, setPracticeHistory] = useState([]);
    const [practiceInput, setPracticeInput] = useState('');
    const practiceEndRef = useRef(null);

    const handlePracticeSend = async (message) => {
        if (!message.trim()) return;

        const newHistory = [...practiceHistory, { role: 'user', content: message }];
        setPracticeHistory(newHistory);

        try {
            const result = await aiService.practiceChat(message, newHistory, 'random_persona');
            setPracticeHistory([...newHistory, { role: 'assistant', content: result.response }]);
        } catch (error) {
            console.error('Practice chat error:', error);
            setPracticeHistory([...newHistory, { role: 'assistant', content: "..." }]);
        }
    };

    const startPracticeMode = () => {
        setShowPracticeMode(true);
        if (practiceHistory.length === 0) {
            setPracticeHistory([{ role: 'assistant', content: "Hi! I'm a random match based on your preferences. Say hello!" }]);
        }
    };
    const [matching, setMatching] = useState(false);

    const startRandomChat = () => {
        if (!user) {
            navigate('/login');
            return;
        }
        setMatching(true);
        // Simulate matching delay for effect
        setTimeout(() => {
            navigate('/random-chat');
        }, 1500);
    };

    return (
        <div className="home-page">
            <div className="hero-section">
                <h1>Ready to <span className="highlight">Spark</span> Something Special? 💕</h1>
                <p className="hero-subtitle">
                    Meet real people, have genuine conversations, and discover your perfect match.
                    It's dating, but actually fun! ✨
                </p>

                <div className="action-buttons">
                    <Link
                        to="/random-chat"
                        className={`btn btn-primary btn-lg ${matching ? 'pulse' : ''}`}
                        onClick={startRandomChat}
                        disabled={matching}
                    >
                        {matching ? '🔍 Finding Someone...' : '🎲 Start Random Chat'}
                    </Link>

                    <button onClick={startPracticeMode} className="btn btn-secondary btn-lg">
                        🤖 Practice Mode
                    </button>

                    {!user && (
                        <button
                            className="btn btn-secondary btn-lg"
                            onClick={() => navigate('/register')}
                        >
                            💖 Join FlirtNet
                        </button>
                    )}
                </div>
            </div>

            <div className="features-grid container">
                <div className="feature-card card">
                    <div className="feature-icon">✨</div>
                    <h3>Random Match</h3>
                    <p>Jump into a chat with someone new. Who knows? They might be your type! 😉</p>
                </div>

                <div className="feature-card card">
                    <div className="feature-icon">🤝</div>
                    <h3>Make it Official</h3>
                    <p>Vibing with someone? Send a datemate request and keep the spark alive! 🔥</p>
                </div>

                <div className="feature-card card">
                    <div className="feature-icon">💡</div>
                    <h3>New to Dating?</h3>
                    <p>No worries, we're here to help! Get AI tips, practice conversations, and boost your confidence! 💪</p>
                </div>
            </div>

            <AIChatModal
                isOpen={showPracticeMode}
                onClose={() => setShowPracticeMode(false)}
                history={practiceHistory}
                onSend={handlePracticeSend}
                inputText={practiceInput}
                setInputText={setPracticeInput}
                messagesEndRef={practiceEndRef}
                title="🤖 Practice Mode"
            />
        </div>
    );
}

export default HomePage;
