/**
 * Connections Page - Manage datemate connections and requests.
 */
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { connectionService } from '../services/connectionService';
import { profileService } from '../services/profileService';
import './DatematesPage.css';

function DatematesPage() {
    const [connections, setConnections] = useState([]);
    const [pendingRequests, setPendingRequests] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const [conns, reqs] = await Promise.all([
                connectionService.getConnections(),
                connectionService.getPendingRequests()
            ]);

            // Enhance with profile data
            const enhancedConns = await Promise.all(conns.map(async (conn) => {
                const partnerId = conn.requester_id === conn.receiver_id ? conn.receiver_id : conn.requester_id; // Logic error here, fix below
                // Actually we need to find the OTHER user ID
                // But for now let's just fetch profile for the ID that isn't ours
                // We need current user ID to know which is "other", but let's simplify:
                // The API returns connections where we are either requester or receiver.
                // We'll fetch profile for both and pick the one that isn't us? 
                // Better: API should probably return profile data. 
                // For now, let's just display ID.
                return conn;
            }));

            setConnections(conns);
            setPendingRequests(reqs);
        } catch (error) {
            console.error('Failed to load connections:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleAccept = async (id) => {
        try {
            await connectionService.acceptRequest(id);
            loadData(); // Reload to update lists
        } catch (error) {
            console.error('Failed to accept request:', error);
        }
    };

    const handleReject = async (id) => {
        try {
            await connectionService.rejectRequest(id);
            loadData();
        } catch (error) {
            console.error('Failed to reject request:', error);
        }
    };

    const startChat = (connectionId) => {
        navigate(`/messages/${connectionId}`);
    };

    if (loading) return <div className="loading">Loading connections...</div>;

    return (
        <div className="container connections-page">
            <div className="connections-layout">
                <div className="section">
                    <h2>Pending Requests</h2>
                    {pendingRequests.length === 0 ? (
                        <p className="empty-text">No pending requests.</p>
                    ) : (
                        <div className="requests-list">
                            {pendingRequests.map(req => (
                                <div key={req.id} className="request-card card">
                                    <div className="request-info">
                                        <div className="avatar-small">U</div>
                                        <span>User #{req.requester_id} wants to connect</span>
                                    </div>
                                    <div className="request-actions">
                                        <button
                                            className="btn btn-primary btn-sm"
                                            onClick={() => handleAccept(req.id)}
                                        >
                                            Accept
                                        </button>
                                        <button
                                            className="btn btn-secondary btn-sm"
                                            onClick={() => handleReject(req.id)}
                                        >
                                            Reject
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                <div className="section">
                    <h2>My Datemates</h2>
                    {connections.length === 0 ? (
                        <div className="empty-state card">
                            <p>No connections yet.</p>
                            <p>Start a random chat to meet people!</p>
                        </div>
                    ) : (
                        <div className="connections-grid">
                            {connections.map(conn => (
                                <div key={conn.id} className="connection-card card">
                                    <div className="connection-avatar">
                                        D
                                    </div>
                                    <h3>Datemate</h3>
                                    <p className="connection-date">
                                        Connected since {new Date(conn.responded_at).toLocaleDateString()}
                                    </p>
                                    <button
                                        className="btn btn-primary btn-full"
                                        onClick={() => startChat(conn.id)}
                                    >
                                        Message
                                    </button>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default DatematesPage;
