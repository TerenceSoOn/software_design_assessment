/**
 * Header Component - Navigation bar
 */
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './Header.css';

function Header() {
    const { user, profile, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

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
                            <Link to="/login" className="btn btn-primary btn-sm">
                                Login
                            </Link>
                        </>
                    )}
                </nav>
            </div>
        </header >
    );
}

export default Header;
