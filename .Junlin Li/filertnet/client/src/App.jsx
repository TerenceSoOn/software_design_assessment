import { useState } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  Link,
  useNavigate,
} from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Profile from "./pages/Profile";
import PublicSquare from "./pages/PublicSquare";
import Chat from "./pages/Chat";
import DirectChat from "./pages/DirectChat";
import Connections from "./pages/Connections";
import AICompanion from "./pages/AICompanion";
import "./App.css";

// Wrapper component to use hooks like useNavigate inside the Router context
function AppContent() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();

  const handleLogin = () => {
    setIsAuthenticated(true);
    navigate("/");
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    navigate("/");
  };

  return (
    <div className="app-container">
      <Routes>
        <Route path="/login" element={<Login onLogin={handleLogin} />} />
        <Route path="/register" element={<Register onLogin={handleLogin} />} />

        {/* Protected Routes */}
        <Route
          path="/profile"
          element={isAuthenticated ? <Profile /> : <Navigate to="/login" />}
        />
        <Route
          path="/public-square"
          element={
            isAuthenticated ? <PublicSquare /> : <Navigate to="/login" />
          }
        />
        <Route
          path="/chat"
          element={isAuthenticated ? <Chat /> : <Navigate to="/login" />}
        />
        <Route
          path="/chat/:userId"
          element={isAuthenticated ? <DirectChat /> : <Navigate to="/login" />}
        />
        <Route
          path="/connections"
          element={isAuthenticated ? <Connections /> : <Navigate to="/login" />}
        />
        <Route
          path="/ai-companion"
          element={isAuthenticated ? <AICompanion /> : <Navigate to="/login" />}
        />

        <Route
          path="/"
          element={
            <div className="card">
              <h1>FlirtNet</h1>
              <p>Welcome to FlirtNet - A caring social platform.</p>

              <div className="home-content">
                {!isAuthenticated ? (
                  // Guest View
                  <>
                    <p>Please log in to continue.</p>
                    <div className="guest-actions">
                      <Link to="/login">
                        <button className="home-btn primary">Login</button>
                      </Link>
                      <Link to="/register">
                        <button className="home-btn">Register</button>
                      </Link>
                    </div>
                  </>
                ) : (
                  // Logged In View
                  <>
                    <p className="welcome-text">You are logged in!</p>
                    <div className="home-buttons-grid">
                      <Link to="/public-square">
                        <button className="home-btn">Public Square</button>
                      </Link>
                      <Link to="/chat">
                        <button className="home-btn">Random Chat</button>
                      </Link>
                      <Link to="/connections">
                        <button className="home-btn">Connections</button>
                      </Link>
                      <Link to="/ai-companion">
                        <button className="home-btn">AI Companion</button>
                      </Link>
                      <Link to="/profile" className="full-width">
                        <button className="home-btn full-width">
                          My Profile
                        </button>
                      </Link>
                    </div>
                    <button onClick={handleLogout} className="home-btn logout">
                      Logout
                    </button>
                  </>
                )}
              </div>
            </div>
          }
        />
      </Routes>
    </div>
  );
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;
