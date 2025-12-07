import React from 'react';

/**
 * AI Chat Modal Component
 * Reusable modal for AI interactions (Companion, Practice Mode, etc.)
 */
const AIChatModal = ({ isOpen, onClose, history, onSend, inputText, setInputText, messagesEndRef, title = "🤖 AI Companion" }) => {
    if (!isOpen) return null;

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!inputText.trim()) return;
        // Pass the message text to onSend, not the event
        onSend(inputText);
        // Clear input after sending
        setInputText('');
    };

    return (
        <div className="modal-overlay">
            <div className="modal-content ai-chat-modal">
                <div className="modal-header">
                    <h3>{title}</h3>
                    <button className="close-btn" onClick={onClose}>&times;</button>
                </div>
                <div className="modal-body">
                    <div className="ai-messages" style={{ flex: 1, overflowY: 'auto', marginBottom: '15px' }}>
                        {history.map((msg, idx) => (
                            <div key={idx} className={`message ${msg.role === 'user' ? 'me' : 'partner'}`}>
                                <div className="message-bubble">
                                    {msg.content}
                                </div>
                            </div>
                        ))}
                        <div ref={messagesEndRef} />
                    </div>
                    <form onSubmit={handleSubmit} className="chat-input-area" style={{ display: 'flex', gap: '10px' }}>
                        <input
                            type="text"
                            className="input chat-input"
                            placeholder="Type a message..."
                            value={inputText}
                            onChange={(e) => setInputText(e.target.value)}
                            style={{ flex: 1 }}
                        />
                        <button type="submit" className="btn btn-primary">Send</button>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default AIChatModal;

