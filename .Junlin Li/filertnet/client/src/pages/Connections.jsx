import { useState } from "react";
import { Link } from "react-router-dom";
import "./Connections.css";

function Connections() {
  // Mock data for connections
  const [connections, setConnections] = useState([
    {
      id: 1,
      name: "Sarah Connor",
      avatar: "https://via.placeholder.com/50",
      status: "Online",
      lastMessage: "See you tomorrow!",
    },
    {
      id: 2,
      name: "John Doe",
      avatar: "https://via.placeholder.com/50",
      status: "Offline",
      lastMessage: "Thanks for the help.",
    },
  ]);

  // Mock data for pending requests
  const [requests, setRequests] = useState([
    {
      id: 3,
      name: "New Friend",
      avatar: "https://via.placeholder.com/50",
      mutualFriends: 2,
    },
  ]);

  const handleAccept = (id) => {
    const request = requests.find((r) => r.id === id);
    if (request) {
      setConnections([
        ...connections,
        { ...request, status: "Online", lastMessage: "You are now connected!" },
      ]);
      setRequests(requests.filter((r) => r.id !== id));
    }
  };

  const handleReject = (id) => {
    setRequests(requests.filter((r) => r.id !== id));
  };

  return (
    <div className="connections-container">
      <Link to="/" className="back-link">
        &larr; Back to Home
      </Link>
      <div className="connections-header">
        <h2>My Connections</h2>
      </div>

      {/* Pending Requests Section */}
      {requests.length > 0 && (
        <>
          <h3 className="section-title">
            Pending Requests ({requests.length})
          </h3>
          <div className="connections-list">
            {requests.map((req) => (
              <div key={req.id} className="connection-card">
                <img
                  src={req.avatar}
                  alt={req.name}
                  className="connection-avatar"
                />
                <div className="connection-info">
                  <h4 className="connection-name">{req.name}</h4>
                  <p className="connection-status">
                    {req.mutualFriends} mutual friends
                  </p>
                </div>
                <div className="connection-actions">
                  <button
                    className="action-button btn-accept"
                    onClick={() => handleAccept(req.id)}
                  >
                    Accept
                  </button>
                  <button
                    className="action-button btn-reject"
                    onClick={() => handleReject(req.id)}
                  >
                    Reject
                  </button>
                </div>
              </div>
            ))}
          </div>
        </>
      )}

      {/* Active Connections Section */}
      <h3 className="section-title">All Connections ({connections.length})</h3>

      {connections.length === 0 ? (
        <div className="empty-state">
          <p>You haven't connected with anyone yet.</p>
          <Link
            to="/chat"
            style={{
              color: "#646cff",
              marginTop: "1rem",
              display: "inline-block",
            }}
          >
            Go find some friends!
          </Link>
        </div>
      ) : (
        <div className="connections-list">
          {connections.map((conn) => (
            <div key={conn.id} className="connection-card">
              <img
                src={conn.avatar}
                alt={conn.name}
                className="connection-avatar"
              />
              <div className="connection-info">
                <h4 className="connection-name">{conn.name}</h4>
                <p
                  className={`connection-status ${
                    conn.status === "Online" ? "online" : ""
                  }`}
                >
                  {conn.status} • {conn.lastMessage}
                </p>
              </div>
              <div className="connection-actions">
                <Link
                  to={`/chat/${conn.id}`}
                  className="action-button btn-chat"
                  style={{
                    textDecoration: "none",
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  Chat
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Connections;
