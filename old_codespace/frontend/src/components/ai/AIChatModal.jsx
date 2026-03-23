import React from 'react';
import './AIChatModal.css';

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
        <div className="ai-chat-overlay" onClick={onClose}>
            <div className="modal-content ai-chat-modal" onClick={e => e.stopPropagation()}>
                <div className="ai-modal-header">
                    <h3>{title}</h3>
                    <button className="ai-close-btn" onClick={onClose}>&times;</button>
                </div>
                <div className="ai-modal-body">
                    <div className="ai-messages">
                        {history.map((msg, idx) => (
                            <div key={idx} className={`message ${msg.role === 'user' ? 'me' : 'partner'}`}>
                                <div className="message-bubble">
                                    {msg.content}
                                </div>
                            </div>
                        ))}
                        <div ref={messagesEndRef} />
                    </div>
                    <form onSubmit={handleSubmit} className="chat-input-area">
                        <input
                            type="text"
                            className="chat-input"
                            placeholder="Type a message..."
                            value={inputText}
                            onChange={(e) => setInputText(e.target.value)}
                        />
                        <button type="submit" className="btn btn-primary">Send</button>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default AIChatModal;

