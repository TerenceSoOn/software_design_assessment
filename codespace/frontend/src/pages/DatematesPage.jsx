/**
 * Connections Page - Manage datemate connections and requests.
 */
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { datemateService } from '../services/datemateService';
import { profileService } from '../services/profileService';
import { useAuth } from '../context/AuthContext';
import './DatematesPage.css';

function DatematesPage() {
    const { user } = useAuth();
    const [datemates, setDatemates] = useState([]);
    const [pendingRequests, setPendingRequests] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const [datematesData, requestsData] = await Promise.all([
                datemateService.getDatemates(),
                datemateService.getPendingRequests()
            ]);

            // Fetch partner profiles for datemates
            const datematesWithProfiles = await Promise.all(
                datematesData.map(async (conn) => {
                    try {
                        // Determine who the partner is based on current user
                        const partnerId = conn.requester_id === user?.id ? conn.receiver_id : conn.requester_id;
                        if (partnerId) {
                            const profile = await profileService.getProfile(partnerId);
                            return { ...conn, partnerProfile: profile, partnerId };
                        }
                    } catch (e) {
                        console.error('Failed to load profile for datemate:', e);
                    }
                    return conn;
                })
            );

            // Fetch requester profiles for pending requests
            const requestsWithProfiles = await Promise.all(
                requestsData.map(async (req) => {
                    try {
                        if (req.requester_id) {
                            const profile = await profileService.getProfile(req.requester_id);
                            return { ...req, requesterProfile: profile };
                        }
                    } catch (e) {
                        console.error('Failed to load profile for request:', e);
                    }
                    return req;
                })
            );

            setDatemates(datematesWithProfiles);
            setPendingRequests(requestsWithProfiles);
        } catch (error) {
            console.error('Failed to load datemates:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleAccept = async (id) => {
        try {
            await datemateService.acceptRequest(id);
            loadData(); // Reload to update lists
        } catch (error) {
            console.error('Failed to accept request:', error);
        }
    };

    const handleReject = async (id) => {
        try {
            await datemateService.rejectRequest(id);
            loadData();
        } catch (error) {
            console.error('Failed to reject request:', error);
        }
    };

    const startChat = (datemateId) => {
        navigate(`/messages/${datemateId}`);
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
                                        <div className="avatar-small" style={{
                                            backgroundColor: '#FF69B4',
                                            color: 'white',
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center',
                                            width: '40px',
                                            height: '40px',
                                            borderRadius: '50%',
                                            fontWeight: 'bold'
                                        }}>
                                            {req.requesterProfile?.display_name?.[0]?.toUpperCase() || 'U'}
                                        </div>
                                        <span>{req.requesterProfile?.display_name || `User #${req.requester_id}`} wants to connect</span>
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
                    {datemates.length === 0 ? (
                        <div className="empty-state card">
                            <p>No connections yet.</p>
                            <p>Start a random chat to meet people!</p>
                        </div>
                    ) : (
                        <div className="connections-grid">
                            {datemates.map(conn => (
                                <div key={conn.id} className="connection-card card">
                                    <div className="connection-avatar" style={{
                                        backgroundColor: '#FF69B4',
                                        color: 'white',
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        width: '80px',
                                        height: '80px',
                                        borderRadius: '50%',
                                        fontWeight: 'bold',
                                        fontSize: '2rem',
                                        margin: '0 auto 15px'
                                    }}>
                                        {conn.partnerProfile?.display_name?.[0]?.toUpperCase() || 'D'}
                                    </div>
                                    <h3>{conn.partnerProfile?.display_name || 'Datemate'}</h3>
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
