import React from 'react';

function WingmanModal({ isOpen, onClose, atmosphere, suggestions, onSelectSuggestion }) {
    if (!isOpen) return null;

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content ai-chat-modal" onClick={e => e.stopPropagation()} style={{ maxWidth: '600px' }}>
                <div className="modal-header" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
                    <h3 style={{ margin: 0, fontSize: '1.3rem', fontWeight: '600' }}>💡 Wingman Coach</h3>
                    <button className="close-btn" onClick={onClose} style={{ color: 'white', fontSize: '1.8rem' }}>&times;</button>
                </div>
                <div className="modal-body" style={{ padding: '24px' }}>
                    {atmosphere && (
                        <div style={{
                            background: 'linear-gradient(135deg, rgba(255, 107, 157, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)',
                            padding: '18px',
                            borderRadius: '16px',
                            border: '1px solid rgba(102, 126, 234, 0.2)',
                            marginBottom: '24px',
                            boxShadow: '0 2px 8px rgba(0,0,0,0.05)'
                        }}>
                            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '12px' }}>
                                <span style={{ fontSize: '1.5rem', marginRight: '8px' }}>📊</span>
                                <h4 style={{ margin: 0, color: '#667eea', fontSize: '1.1rem', fontWeight: '600' }}>Current Vibe</h4>
                            </div>
                            <p style={{ margin: 0, fontSize: '0.95rem', color: '#555', lineHeight: '1.6' }}>
                                {atmosphere.feedback || atmosphere.analysis || (typeof atmosphere === 'string' ? atmosphere : 'Analyzing...')}
                            </p>
                        </div>
                    )}

                    <div>
                        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '16px' }}>
                            <span style={{ fontSize: '1.5rem', marginRight: '8px' }}>💬</span>
                            <h4 style={{ margin: 0, color: '#333', fontSize: '1.1rem', fontWeight: '600' }}>Try saying this...</h4>
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                            {suggestions && suggestions.length > 0 ? (
                                suggestions.map((sug, i) => (
                                    <button
                                        key={i}
                                        onClick={() => onSelectSuggestion(sug)}
                                        style={{
                                            textAlign: 'left',
                                            padding: '16px 18px',
                                            fontSize: '0.95rem',
                                            background: 'white',
                                            border: '2px solid #e0e0e0',
                                            borderRadius: '12px',
                                            cursor: 'pointer',
                                            transition: 'all 0.2s ease',
                                            color: '#333',
                                            lineHeight: '1.5',
                                            fontWeight: '400',
                                            position: 'relative',
                                            paddingLeft: '48px'
                                        }}
                                        onMouseEnter={(e) => {
                                            e.target.style.borderColor = '#667eea';
                                            e.target.style.background = 'rgba(102, 126, 234, 0.05)';
                                            e.target.style.transform = 'translateX(4px)';
                                        }}
                                        onMouseLeave={(e) => {
                                            e.target.style.borderColor = '#e0e0e0';
                                            e.target.style.background = 'white';
                                            e.target.style.transform = 'translateX(0)';
                                        }}
                                    >
                                        <span style={{
                                            position: 'absolute',
                                            left: '18px',
                                            top: '50%',
                                            transform: 'translateY(-50%)',
                                            fontSize: '1.2rem',
                                            color: '#667eea',
                                            fontWeight: '700'
                                        }}>{i + 1}</span>
                                        {sug}
                                    </button>
                                ))
                            ) : (
                                <p style={{ color: '#999', textAlign: 'center', padding: '20px' }}>Loading suggestions...</p>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default WingmanModal;
