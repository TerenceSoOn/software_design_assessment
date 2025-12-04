/**
 * Profile Page - View and edit user profile.
 */
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { profileService } from '../services/profileService';
import './ProfilePage.css';

function ProfilePage() {
    const { profile, updateUserProfile } = useAuth();
    const [isEditing, setIsEditing] = useState(false);
    const [formData, setFormData] = useState({
        display_name: '',
        bio: '',
        age: '',
        gender: '',
        location: '',
        interests: '',
    });
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        if (profile) {
            setFormData({
                display_name: profile.display_name || '',
                bio: profile.bio || '',
                age: profile.age || '',
                gender: profile.gender || '',
                location: profile.location || '',
                interests: profile.interests ? profile.interests.join(', ') : '',
            });
        }
    }, [profile]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const updatedData = {
                ...formData,
                age: formData.age ? parseInt(formData.age) : null,
                interests: formData.interests.split(',').map(i => i.trim()).filter(i => i),
            };

            const updatedProfile = await profileService.updateProfile(updatedData);
            updateUserProfile(updatedProfile);
            setIsEditing(false);
        } catch (error) {
            console.error('Failed to update profile:', error);
            alert('Failed to update profile');
        } finally {
            setLoading(false);
        }
    };

    if (!profile) return <div className="loading">Loading profile...</div>;

    return (
        <div className="container">
            <div className="profile-layout">
                <div className="profile-sidebar card">
                    <div className="avatar-container">
                        <div className="avatar-placeholder">
                            {profile.display_name ? profile.display_name[0].toUpperCase() : 'U'}
                        </div>
                    </div>
                    <h2>{profile.display_name || 'User'}</h2>
                    <p className="username">@{profile.user_id}</p>

                    <div className="profile-stats">
                        <div className="stat">
                            <span className="stat-value">0</span>
                            <span className="stat-label">Posts</span>
                        </div>
                        <div className="stat">
                            <span className="stat-value">0</span>
                            <span className="stat-label">Friends</span>
                        </div>
                    </div>
                </div>

                <div className="profile-content card">
                    <div className="content-header">
                        <h3>Profile Details</h3>
                        {!isEditing && (
                            <div className="header-actions">
                                <button className="btn btn-secondary btn-sm" onClick={() => setIsEditing(true)}>
                                    Edit Profile
                                </button>
                                <button
                                    className="btn btn-primary btn-sm"
                                    onClick={() => navigate('/ai-companion')}
                                    title="Get AI tips to improve your profile"
                                >
                                    ✨ Optimize with AI
                                </button>
                            </div>
                        )}
                    </div>

                    {isEditing ? (
                        <form onSubmit={handleSubmit} className="profile-form">
                            <div className="form-group">
                                <label>Display Name</label>
                                <input
                                    type="text"
                                    name="display_name"
                                    className="input"
                                    value={formData.display_name}
                                    onChange={handleChange}
                                />
                            </div>

                            <div className="form-group">
                                <label>Bio</label>
                                <textarea
                                    name="bio"
                                    className="input textarea"
                                    value={formData.bio}
                                    onChange={handleChange}
                                    rows="4"
                                />
                            </div>

                            <div className="form-row">
                                <div className="form-group">
                                    <label>Age</label>
                                    <input
                                        type="number"
                                        name="age"
                                        className="input"
                                        value={formData.age}
                                        onChange={handleChange}
                                    />
                                </div>
                                <div className="form-group">
                                    <label>Gender</label>
                                    <select
                                        name="gender"
                                        className="input"
                                        value={formData.gender}
                                        onChange={handleChange}
                                    >
                                        <option value="">Select...</option>
                                        <option value="Male">Male</option>
                                        <option value="Female">Female</option>
                                        <option value="Non-binary">Non-binary</option>
                                        <option value="Other">Other</option>
                                    </select>
                                </div>
                            </div>

                            <div className="form-group">
                                <label>Location</label>
                                <input
                                    type="text"
                                    name="location"
                                    className="input"
                                    value={formData.location}
                                    onChange={handleChange}
                                />
                            </div>

                            <div className="form-group">
                                <label>Interests (comma separated)</label>
                                <input
                                    type="text"
                                    name="interests"
                                    className="input"
                                    value={formData.interests}
                                    onChange={handleChange}
                                    placeholder="Music, Travel, Coding..."
                                />
                            </div>

                            <div className="form-actions">
                                <button type="button" className="btn btn-secondary" onClick={() => setIsEditing(false)}>
                                    Cancel
                                </button>
                                <button type="submit" className="btn btn-primary" disabled={loading}>
                                    {loading ? 'Saving...' : 'Save Changes'}
                                </button>
                            </div>
                        </form>
                    ) : (
                        <div className="profile-info">
                            <div className="info-group">
                                <label>Bio</label>
                                <p>{profile.bio || 'No bio yet.'}</p>
                            </div>

                            <div className="info-row">
                                <div className="info-group">
                                    <label>Age</label>
                                    <p>{profile.age || '-'}</p>
                                </div>
                                <div className="info-group">
                                    <label>Gender</label>
                                    <p>{profile.gender || '-'}</p>
                                </div>
                                <div className="info-group">
                                    <label>Location</label>
                                    <p>{profile.location || '-'}</p>
                                </div>
                            </div>

                            <div className="info-group">
                                <label>Interests</label>
                                <div className="tags">
                                    {profile.interests && profile.interests.length > 0 ? (
                                        profile.interests.map((tag, index) => (
                                            <span key={index} className="tag">{tag}</span>
                                        ))
                                    ) : (
                                        <p>-</p>
                                    )}
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default ProfilePage;
