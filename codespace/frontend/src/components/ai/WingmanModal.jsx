import React from 'react';
import './WingmanModal.css';

function WingmanModal({ isOpen, onClose, atmosphere, suggestions, onSelectSuggestion }) {
    if (!isOpen) return null;

    return (
        <div className="wingman-overlay" onClick={onClose}>
            <div className="modal-content wingman-modal" onClick={e => e.stopPropagation()}>
                <div className="wingman-header">
                    <h3>💡 Your Wingman</h3>
                    <button className="wingman-close-btn" onClick={onClose}>&times;</button>
                </div>

                <div className="wingman-body">
                    {atmosphere && (
                        <div className="vibe-section">
                            <div className="vibe-header">
                                <span className="vibe-icon">📊</span>
                                <h4>Current Vibe</h4>
                            </div>
                            <p className="vibe-text">
                                {atmosphere.feedback || atmosphere.analysis || (typeof atmosphere === 'string' ? atmosphere : 'Analyzing...')}
                            </p>
                        </div>
                    )}

                    <div className="suggestions-section">
                        <div className="suggestions-header">
                            <span className="vibe-icon">💬</span>
                            <h4>Try saying this...</h4>
                        </div>

                        <div className="suggestions-list">
                            {suggestions && suggestions.length > 0 ? (
                                suggestions.map((sug, i) => (
                                    <button
                                        key={i}
                                        className="suggestion-card"
                                        onClick={() => onSelectSuggestion(sug)}
                                    >
                                        <div className="suggestion-number">{i + 1}</div>
                                        {sug}
                                    </button>
                                ))
                            ) : (
                                <p className="loading-text">Loading suggestions...</p>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default WingmanModal;
