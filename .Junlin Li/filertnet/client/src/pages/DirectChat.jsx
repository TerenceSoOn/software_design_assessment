import { useState, useEffect, useRef } from "react";
import { Link, useParams } from "react-router-dom";
import "./Chat.css"; // Reusing Chat styles

function DirectChat() {
  const { userId } = useParams();
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const messagesEndRef = useRef(null);

  // Mock user data based on ID
  const partnerName = userId === "1" ? "Sarah Connor" : "John Doe";
  const isOnline = userId === "1";

  // Auto-scroll to bottom of chat
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    // Simulate loading chat history
    const history = [
      {
        id: 1,
        type: "received",
        text: "Hey! How are you doing?",
        time: "10:00 AM",
      },
      {
        id: 2,
        type: "sent",
        text: "I'm doing great, thanks! How about you?",
        time: "10:05 AM",
      },
      {
        id: 3,
        type: "received",
        text: userId === "1" ? "See you tomorrow!" : "Thanks for the help.",
        time: "10:10 AM",
      },
    ];
    setMessages(history);
  }, [userId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const newMessage = {
      id: Date.now(),
      type: "sent",
      text: inputValue,
      time: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    };

    setMessages((prev) => [...prev, newMessage]);
    setInputValue("");

    // Simulate receiving a reply
    setTimeout(() => {
      const replyMessage = {
        id: Date.now() + 1,
        type: "received",
        text: "Got it! I'll get back to you soon.",
        time: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      };
      setMessages((prev) => [...prev, replyMessage]);
    }, 1500);
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="chat-partner-info">
          <Link
            to="/connections"
            className="back-link"
            style={{ marginRight: "1rem", marginBottom: 0 }}
          >
            &larr;
          </Link>
          <h3>{partnerName}</h3>
          <span
            className="chat-status"
            style={{ marginLeft: "10px", color: isOnline ? "#4caf50" : "#888" }}
          >
            ● {isOnline ? "Online" : "Offline"}
          </span>
        </div>
      </div>

      <div className="messages-area">
        {messages.map((msg) => (
          <div key={msg.id} className={`message ${msg.type}`}>
            {msg.text}
            {msg.time && <span className="message-time">{msg.time}</span>}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-area" onSubmit={handleSendMessage}>
        <input
          type="text"
          placeholder="Type a message..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          autoFocus
        />
        <button
          type="submit"
          className="send-button"
          disabled={!inputValue.trim()}
        >
          ➤
        </button>
      </form>
    </div>
  );
}

export default DirectChat;
