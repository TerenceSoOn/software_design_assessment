/**
 * Messages Page - Private messaging with datemates.
 */
import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './MessagesPage.css';

function MessagesPage() {
    const { connectionId } = useParams();
    const [messages, setMessages] = useState([]);
    const [inputText, setInputText] = useState('');

    // Mock loading messages
    useEffect(() => {
        if (connectionId) {
            setMessages([
                { id: 1, sender: 'partner', text: 'Hey! Glad we connected.' },
                { id: 2, sender: 'me', text: 'Me too! That was a fun chat.' }
            ]);
        }
    }, [connectionId]);

    const handleSend = (e) => {
        e.preventDefault();
        if (!inputText.trim()) return;

        const newMsg = {
            id: Date.now(),
            sender: 'me',
            text: inputText
        };
        setMessages([...messages, newMsg]);
        setInputText('');
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
            <div className="messages-card card">
                <div className="messages-header">
                    <h3>Datemate Chat</h3>
                </div>

                <div className="messages-list">
                    {messages.map(msg => (
                        <div key={msg.id} className={`msg-row ${msg.sender}`}>
                            <div className="msg-bubble">
                                {msg.text}
                            </div>
                        </div>
                    ))}
                </div>

                <form onSubmit={handleSend} className="msg-input-area">
                    <input
                        type="text"
                        className="input"
                        value={inputText}
                        onChange={(e) => setInputText(e.target.value)}
                        placeholder="Type a message..."
                    />
                    <button type="submit" className="btn btn-primary">Send</button>
                </form>
            </div>
        </div>
    );
}

export default MessagesPage;
