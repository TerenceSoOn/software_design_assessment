import { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import "./Chat.css";

function Chat() {
  const [isMatching, setIsMatching] = useState(false);
  const [isChatting, setIsChatting] = useState(false);
  const [isRequestSent, setIsRequestSent] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom of chat
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const startMatching = () => {
    setIsMatching(true);
    setIsRequestSent(false);

    // Simulate finding a match after 2 seconds
    setTimeout(() => {
      setIsMatching(false);
      setIsChatting(true);
      setMessages([
        {
          id: 1,
          type: "system",
          text: "You are now connected with a stranger. Say hi!",
        },
      ]);
    }, 2000);
  };

  const handleConnect = () => {
    setIsRequestSent(true);
    // Simulate sending request
    const systemMsg = {
      id: Date.now(),
      type: "system",
      text: "Connection request sent!",
    };
    setMessages((prev) => [...prev, systemMsg]);
  };

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

    // Simulate receiving a reply after 1-3 seconds
    setTimeout(() => {
      const replies = [
        "That's interesting!",
        "Tell me more.",
        "I totally agree with you.",
        "Haha, really?",
        "I'm from the other side of the world!",
        "Do you like coding?",
      ];
      const randomReply = replies[Math.floor(Math.random() * replies.length)];

      const replyMessage = {
        id: Date.now() + 1,
        type: "received",
        text: randomReply,
        time: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      };

      setMessages((prev) => [...prev, replyMessage]);
    }, Math.random() * 2000 + 1000);
  };

  const leaveChat = () => {
    if (window.confirm("Are you sure you want to leave this conversation?")) {
      setIsChatting(false);
      setMessages([]);
    }
  };

  if (!isChatting) {
    return (
      <div className="chat-container">
        <Link to="/" className="back-link" style={{ margin: "1rem" }}>
          &larr; Back to Home
        </Link>
        <div className="matching-screen">
          {isMatching ? (
            <>
              <div className="spinner"></div>
              <h2>Finding a partner...</h2>
              <p>Looking for someone who shares your interests.</p>
            </>
          ) : (
            <>
              <h2>Ready to Chat?</h2>
              <p>
                Meet new people randomly. Conversations are anonymous until you
                decide to connect.
              </p>
              <button className="match-button" onClick={startMatching}>
                Start Random Chat
              </button>
            </>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="chat-partner-info">
          <h3>Stranger</h3>
          <span className="chat-status" style={{ marginLeft: "10px" }}>
            ● Online
          </span>
        </div>
        <div style={{ display: "flex", gap: "10px" }}>
          {!isRequestSent ? (
            <button
              className="leave-button"
              style={{ borderColor: "#4caf50", color: "#4caf50" }}
              onClick={handleConnect}
            >
              Add Friend
            </button>
          ) : (
            <span
              style={{
                color: "#4caf50",
                fontSize: "0.9rem",
                alignSelf: "center",
              }}
            >
              Request Sent ✓
            </span>
          )}
          <button className="leave-button" onClick={leaveChat}>
            Leave Chat
          </button>
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

export default Chat;
