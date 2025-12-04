/**
 * Home Page - Landing page and Random Chat entry point.
 */
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './HomePage.css';

function HomePage() {
    const { user } = useAuth();
    const navigate = useNavigate();
    const [matching, setMatching] = useState(false);

    const startRandomChat = () => {
        if (!user) {
            navigate('/login');
            return;
        }
        setMatching(true);
        // Simulate matching delay for effect
        setTimeout(() => {
            navigate('/chat/random');
        }, 1500);
    };

    return (
        <div className="home-page">
            <div className="hero-section">
                <h1>Find Your Perfect <span className="highlight">Connection</span></h1>
                <p className="hero-subtitle">
                    Experience a dating platform that truly cares.
                    Connect deeply, chat freely, and find meaningful relationships.
                </p>

                <div className="action-buttons">
                    <button
                        className={`btn btn-primary btn-lg ${matching ? 'pulse' : ''}`}
                        onClick={startRandomChat}
                        disabled={matching}
                    >
                        {matching ? 'Finding a Match...' : 'Start Random Chat'}
                    </button>

                    {!user && (
                        <button
                            className="btn btn-secondary btn-lg"
                            onClick={() => navigate('/register')}
                        >
                            Join FlirtNet
                        </button>
                    )}
                </div>
            </div>

            <div className="features-grid container">
                <div className="feature-card card">
                    <div className="feature-icon">✨</div>
                    <h3>Random Match</h3>
                    <p>Meet new people instantly with our caring matching system.</p>
                </div>

                <div className="feature-card card">
                    <div className="feature-icon">🤝</div>
                    <h3>Deep Connections</h3>
                    <p>Turn good chats into lasting Datemate with Datemate requests.</p>
                </div>

                <div className="feature-card card">
                    <div className="feature-icon">🤖</div>
                    <h3>AI Companion</h3>
                    <p>Never feel lonely with our supportive AI assistant always ready to chat.</p>
                </div>
            </div>
        </div>
    );
}

export default HomePage;
