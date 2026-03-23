/**
 * Header Component - Navigation bar
 */
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './Header.css';

function Header() {
    const { user, profile, logout } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    // Determine which auth button to show based on current page
    const isOnLoginPage = location.pathname === '/login';
    const isOnRegisterPage = location.pathname === '/register';

    return (
        <header className="header">
            <div className="header-container">
                <Link to="/" className="logo">
                    <h1>💕 FlirtNet</h1>
                </Link>

                <nav className="nav">
                    {user ? (
                        <>
                            <Link to="/" className="nav-link">
                                Home
                            </Link>
                            <Link to="/square" className="nav-link">
                                🌟 Community
                            </Link>
                            <Link to="/datemates" className="nav-link">
                                💑 My Dates
                            </Link>
                            <Link to="/profile" className="nav-link">
                                Profile
                            </Link>
                            <button onClick={handleLogout} className="btn btn-secondary btn-sm">
                                Logout
                            </button>
                        </>
                    ) : (
                        <>
                            {isOnLoginPage ? (
                                <Link to="/register" className="btn btn-primary btn-sm">
                                    Register
                                </Link>
                            ) : isOnRegisterPage ? (
                                <Link to="/login" className="btn btn-primary btn-sm">
                                    Login
                                </Link>
                            ) : (
                                <Link to="/login" className="btn btn-primary btn-sm">
                                    Login
                                </Link>
                            )}
                        </>
                    )}
                </nav>
            </div>
        </header >
    );
}

export default Header;

