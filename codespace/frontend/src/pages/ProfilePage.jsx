/**
 * Profile Page - View and edit user profile.
 */
import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { profileService } from '../services/profileService';
import { aiService } from '../services/aiService';
import './ProfilePage.css';

function ProfilePage() {
    const { profile, updateUserProfile } = useAuth();
    const [isEditing, setIsEditing] = useState(false);
    const [formData, setFormData] = useState({
        display_name: '',
        bio: '',
        age: '',
        gender: '',
        preferred_gender: '',
        location: '',
        interests: '',
    });
    const [loading, setLoading] = useState(false);
    const [aiSuggestions, setAiSuggestions] = useState(null);
    const [loadingAI, setLoadingAI] = useState(false);

    const navigate = useNavigate();

    const fileInputRef = useRef(null);

    useEffect(() => {
        if (profile) {
            setFormData({
                display_name: profile.display_name || '',
                bio: profile.bio || '',
                age: profile.age || '',
                gender: profile.gender || '',
                preferred_gender: profile.preferred_gender || '',
                location: profile.location || '',
                interests: profile.interests ? profile.interests.join(', ') : '',
            });
        }
    }, [profile]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleAvatarClick = () => {
        if (isEditing) {
            fileInputRef.current?.click();
        }
    };

    const handleFileChange = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        try {
            setLoading(true);
            const { url } = await profileService.uploadAvatar(file);
            // Update profile with new avatar URL
            const updatedProfile = await profileService.updateProfile({ ...profile, avatar_url: url });
            updateUserProfile(updatedProfile);
        } catch (error) {
            console.error("Failed to upload avatar:", error);
            alert("Failed to upload avatar");
        } finally {
            setLoading(false);
        }
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

    const handleOptimizeWithAI = async () => {
        if (!profile.bio) {
            alert('Please add a bio first!');
            return;
        }
        setLoadingAI(true);
        try {
            const result = await aiService.optimizeProfile(profile.bio);
            setAiSuggestions(result.suggestions);
        } catch (error) {
            console.error('Failed to get AI suggestions:', error);
            alert('Failed to get AI suggestions');
        } finally {
            setLoadingAI(false);
        }
    };

    if (!profile) return <div className="loading">Loading profile...</div>;

    return (
        <div className="container">
            <div className="profile-layout">
                <div className="profile-sidebar card">
                    <div className="avatar-container" onClick={handleAvatarClick} style={{ cursor: isEditing ? 'pointer' : 'default', position: 'relative' }}>
                        {profile.avatar_url ? (
                            <img src={profile.avatar_url} alt="Avatar" className="profile-avatar" style={{ width: '100px', height: '100px', borderRadius: '50%', objectFit: 'cover' }} />
                        ) : (
                            <div className="avatar-placeholder">
                                {profile.display_name ? profile.display_name[0].toUpperCase() : 'U'}
                            </div>
                        )}
                        {isEditing && (
                            <div className="avatar-overlay" style={{
                                position: 'absolute', bottom: 0, right: 0, background: 'rgba(0,0,0,0.6)',
                                color: 'white', padding: '5px', borderRadius: '50%', fontSize: '0.8rem'
                            }}>
                                📷
                            </div>
                        )}
                        <input
                            type="file"
                            ref={fileInputRef}
                            onChange={handleFileChange}
                            style={{ display: 'none' }}
                            accept="image/*"
                        />
                    </div>
                    <h2>{profile.display_name || 'User'}</h2>
                    <p className="username">@{profile.user_id}</p>
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
                                    onClick={handleOptimizeWithAI}
                                    disabled={loadingAI}
                                    title="Get AI tips to improve your profile"
                                >
                                    {loadingAI ? '🤔 Thinking...' : '✨ Optimize with AI'}
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
                                        <option value="male">Male</option>
                                        <option value="female">Female</option>
                                        <option value="other">Other</option>
                                    </select>
                                </div>
                                <div className="form-group">
                                    <label>Looking For</label>
                                    <select
                                        name="preferred_gender"
                                        className="input"
                                        value={formData.preferred_gender || ''}
                                        onChange={handleChange}
                                    >
                                        <option value="">Select...</option>
                                        <option value="male">Male</option>
                                        <option value="female">Female</option>
                                        <option value="any">Anyone</option>
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
                        <>
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
                                        <p>{profile.gender ? profile.gender.charAt(0).toUpperCase() + profile.gender.slice(1) : '-'}</p>
                                    </div>
                                    <div className="info-group">
                                        <label>Looking For</label>
                                        <p>{profile.preferred_gender ? (profile.preferred_gender === 'any' ? 'Anyone' : profile.preferred_gender.charAt(0).toUpperCase() + profile.preferred_gender.slice(1)) : '-'}</p>
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

                            {aiSuggestions && (
                                <div className="ai-suggestions">
                                    <h4>🤖 AI Suggestions</h4>
                                    <div className="suggestion-box">
                                        <p>{aiSuggestions}</p>
                                        <button
                                            className="btn btn-sm btn-secondary"
                                            onClick={() => setAiSuggestions(null)}
                                        >
                                            Got it!
                                        </button>
                                    </div>
                                </div>
                            )}
                        </>
                    )}
                </div>
            </div>


        </div >
    );
}

export default ProfilePage;
