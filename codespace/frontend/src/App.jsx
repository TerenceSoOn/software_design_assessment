import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import Layout from './components/layout/Layout';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ProfilePage from './pages/ProfilePage';
import SquarePage from './pages/SquarePage';
import DatematesPage from './pages/DatematesPage';
import RandomChatPage from './pages/RandomChatPage';
import MessagesPage from './pages/MessagesPage';


// Protected Route wrapper
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) return <div className="loading">Loading...</div>;

  if (!user) {
    return <Navigate to="/login" />;
  }

  return children;
};

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* Protected Routes */}
        <Route path="/profile" element={
          <ProtectedRoute>
            <ProfilePage />
          </ProtectedRoute>
        } />
        <Route path="/square" element={
          <ProtectedRoute>
            <SquarePage />
          </ProtectedRoute>
        } />
        <Route path="/datemates" element={
          <ProtectedRoute>
            <DatematesPage />
          </ProtectedRoute>
        } />

        <Route path="/random-chat" element={
          <ProtectedRoute>
            <RandomChatPage />
          </ProtectedRoute>
        } />
        <Route path="/messages/:connectionId" element={
          <ProtectedRoute>
            <MessagesPage />
          </ProtectedRoute>
        } />
      </Route>
    </Routes>
  );
}

export default App;
