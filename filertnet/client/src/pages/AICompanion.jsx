import { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import "./AICompanion.css";

function AICompanion() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: "ai",
      text: "Hello! I'm your AI Companion. I'm here to listen, chat, or help you practice your social skills. How are you feeling today?",
    },
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [mode, setMode] = useState("companion"); // companion, wingman, practice
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const newUserMsg = {
      id: Date.now(),
      sender: "user",
      text: inputValue,
    };

    setMessages((prev) => [...prev, newUserMsg]);
    setInputValue("");
    setIsTyping(true);

    // Simulate AI processing time
    setTimeout(() => {
      const aiResponse = generateMockResponse(inputValue, mode);
      const newAiMsg = {
        id: Date.now() + 1,
        sender: "ai",
        text: aiResponse,
      };
      setMessages((prev) => [...prev, newAiMsg]);
      setIsTyping(false);
    }, 1500);
  };

  const generateMockResponse = (input, currentMode) => {
    const lowerInput = input.toLowerCase();

    if (currentMode === "practice") {
      return "That was a good start! You could also try asking about their hobbies to keep the conversation flowing. Try saying: 'What do you do for fun?'";
    }

    if (currentMode === "wingman") {
      return "Based on their profile, they seem to like hiking. You could suggest a trail you know or ask about their favorite hiking spot.";
    }

    // Default Companion Mode
    if (lowerInput.includes("lonely") || lowerInput.includes("sad")) {
      return "I'm sorry to hear that you're feeling this way. Remember that it's okay to have down days. I'm here if you want to vent.";
    }
    if (lowerInput.includes("hello") || lowerInput.includes("hi")) {
      return "Hi there! What's on your mind?";
    }
    return "I see. Tell me more about that. I'm listening.";
  };

  const handleModeChange = (e) => {
    setMode(e.target.value);
    setMessages([
      {
        id: Date.now(),
        sender: "ai",
        text: getWelcomeMessage(e.target.value),
      },
    ]);
  };

  const getWelcomeMessage = (selectedMode) => {
    switch (selectedMode) {
      case "practice":
        return "Entering Practice Mode. I'll pretend to be a stranger, and then give you feedback on your conversation skills.";
      case "wingman":
        return "Wingman Mode active. Paste a profile or a message here, and I'll help you craft the perfect response.";
      default:
        return "Hello! I'm your AI Companion. I'm here to listen, chat, or help you practice your social skills. How are you feeling today?";
    }
  };

  return (
    <div className="ai-container">
      <div className="ai-header">
        <div className="ai-info">
          <Link
            to="/"
            className="back-link"
            style={{ marginRight: "1rem", marginBottom: 0 }}
          >
            &larr;
          </Link>
          <div className="ai-avatar">🤖</div>
          <div className="ai-details">
            <h3>FlirtNet AI</h3>
            <span className="ai-status">Always Online</span>
          </div>
        </div>

        <select
          className="mode-selector"
          value={mode}
          onChange={handleModeChange}
        >
          <option value="companion">Companion Mode</option>
          <option value="practice">Practice Mode</option>
          <option value="wingman">Wingman Mode</option>
        </select>
      </div>

      <div className="ai-messages-area">
        {messages.map((msg) => (
          <div key={msg.id} className={`ai-message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
        {isTyping && <div className="ai-typing-indicator">AI is typing...</div>}
        <div ref={messagesEndRef} />
      </div>

      <form className="ai-input-area" onSubmit={handleSendMessage}>
        <input
          type="text"
          placeholder="Type a message..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          autoFocus
        />
        <button
          type="submit"
          className="ai-send-button"
          disabled={!inputValue.trim()}
        >
          ➤
        </button>
      </form>
    </div>
  );
}

export default AICompanion;
