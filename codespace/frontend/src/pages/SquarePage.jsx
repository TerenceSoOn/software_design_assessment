/**
 * Square Page - Public posts feed with image support and comments.
 */
import { useState, useEffect } from 'react';
import { postService } from '../services/postService';
import { datemateService } from '../services/datemateService';
import { profileService } from '../services/profileService';
import { useAuth } from '../context/AuthContext';
import './SquarePage.css';

function SquarePage() {
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [newPostContent, setNewPostContent] = useState('');
    const [selectedFiles, setSelectedFiles] = useState([]);
    const [uploading, setUploading] = useState(false);
    const [expandedComments, setExpandedComments] = useState({});
    const [comments, setComments] = useState({});
    const [newComment, setNewComment] = useState({});
    const { user } = useAuth();

    // Profile popup state
    const [selectedProfile, setSelectedProfile] = useState(null);
    const [showProfileModal, setShowProfileModal] = useState(false);

    useEffect(() => {
        loadPosts();
    }, []);

    const loadPosts = async () => {
        try {
            const data = await postService.getPosts();
            setPosts(data);
        } catch (error) {
            console.error('Failed to load posts:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleCreatePost = async (e) => {
        e.preventDefault();
        if (!newPostContent.trim()) return;

        setUploading(true);
        try {
            let imageUrls = [];

            // Upload files if any
            if (selectedFiles.length > 0) {
                // We need to implement uploadImage in postService first
                // For now, assuming postService.uploadImage(file) returns { url: ... }
                const uploadPromises = Array.from(selectedFiles).map(file => postService.uploadImage(file));
                const results = await Promise.all(uploadPromises);
                imageUrls = results.map(res => res.url);
            }

            const newPost = await postService.createPost({
                content_text: newPostContent,
                image_urls: imageUrls,
                tags: []
            });
            setPosts([newPost, ...posts]);
            setNewPostContent('');
            setSelectedFiles([]);
        } catch (error) {
            console.error('Failed to create post:', error);
            alert('Failed to create post');
        } finally {
            setUploading(false);
        }
    };

    const handleConnect = async (userId) => {
        if (userId === user.id) return;
        try {
            await datemateService.sendRequest(userId);
            alert('Datemate request sent!');
            setShowProfileModal(false);
        } catch (error) {
            alert('Failed to send request: ' + (error.response?.data?.detail || error.message));
        }
    };

    const handleViewProfile = async (userId) => {
        try {
            const profile = await profileService.getProfile(userId);
            setSelectedProfile(profile);
            setShowProfileModal(true);
        } catch (error) {
            console.error('Failed to load profile:', error);
        }
    };

    const handleLike = async (postId) => {
        try {
            await postService.likePost(postId);
            // Optimistic update
            setPosts(posts.map(post =>
                post.id === postId
                    ? { ...post, like_count: post.like_count + 1 }
                    : post
            ));
        } catch (error) {
            console.error('Failed to like post:', error);
        }
    };

    const toggleComments = async (postId) => {
        if (expandedComments[postId]) {
            // Collapse
            setExpandedComments({ ...expandedComments, [postId]: false });
        } else {
            // Expand and load comments
            setExpandedComments({ ...expandedComments, [postId]: true });
            if (!comments[postId]) {
                try {
                    const postComments = await postService.getComments(postId);
                    setComments({ ...comments, [postId]: postComments });
                } catch (error) {
                    console.error('Failed to load comments:', error);
                }
            }
        }
    };

    const handleAddComment = async (postId) => {
        const commentText = newComment[postId];
        if (!commentText || !commentText.trim()) return;

        try {
            const comment = await postService.addComment(postId, commentText);

            // Update comments
            setComments({
                ...comments,
                [postId]: [...(comments[postId] || []), comment]
            });

            // Update comment count
            setPosts(posts.map(post =>
                post.id === postId
                    ? { ...post, comment_count: post.comment_count + 1 }
                    : post
            ));

            // Clear input
            setNewComment({ ...newComment, [postId]: '' });
        } catch (error) {
            console.error('Failed to add comment:', error);
            alert('Failed to add comment');
        }
    };

    return (
        <div className="square-page">
            <div className="square-header">
                <h1>🌟 Community</h1>
                <p>Share moments, connect with others</p>
            </div>

            <div className="create-post-card">
                <h3>Share your thoughts</h3>
                <form onSubmit={handleCreatePost}>
                    <textarea
                        className="input textarea"
                        placeholder="What's on your mind?"
                        value={newPostContent}
                        onChange={(e) => setNewPostContent(e.target.value)}
                        rows="3"
                    />
                    <div className="file-upload-container mb-20">
                        <label className="btn btn-secondary btn-sm">
                            📷 Add Photos
                            <input
                                type="file"
                                multiple
                                accept="image/*"
                                onChange={(e) => setSelectedFiles(e.target.files)}
                                style={{ display: 'none' }}
                            />
                        </label>
                        {selectedFiles.length > 0 && (
                            <span className="file-count ml-10">
                                {selectedFiles.length} file(s) selected
                            </span>
                        )}
                    </div>
                    <div className="post-actions">
                        <button
                            type="submit"
                            className="btn btn-primary"
                            disabled={!newPostContent.trim() || uploading}
                        >
                            {uploading ? 'Uploading...' : '📝 Post'}
                        </button>
                    </div>
                </form>
            </div>

            {loading ? (
                <div className="loading">Loading posts...</div>
            ) : (
                <div className="posts-list">
                    {posts.map(post => (
                        <div key={post.id} className="post-card">
                            <div className="post-header">
                                {post.author_avatar_url ? (
                                    <img
                                        src={`${post.author_avatar_url}?t=${Date.now()}`}
                                        alt={post.author_name}
                                        className="post-avatar"
                                        onClick={() => handleViewProfile(post.user_id)}
                                        style={{
                                            cursor: 'pointer',
                                            width: '48px',
                                            height: '48px',
                                            borderRadius: '50%',
                                            objectFit: 'cover'
                                        }}
                                        title="View Profile"
                                    />
                                ) : (
                                    <div
                                        className="post-avatar"
                                        onClick={() => handleViewProfile(post.user_id)}
                                        style={{
                                            cursor: 'pointer',
                                            backgroundColor: '#FF69B4',
                                            color: 'white',
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center',
                                            width: '40px',
                                            height: '40px',
                                            borderRadius: '50%',
                                            fontWeight: 'bold'
                                        }}
                                        title="View Profile"
                                    >
                                        {post.author_name?.[0]?.toUpperCase() || 'U'}
                                    </div>
                                )}
                                <div className="post-meta">
                                    <span
                                        className="post-author"
                                        onClick={() => handleViewProfile(post.user_id)}
                                        style={{ cursor: 'pointer' }}
                                    >
                                        {post.author_name || `User #${post.user_id}`}
                                    </span>
                                    <span className="post-time">
                                        {new Date(post.created_at).toLocaleDateString()}
                                    </span>
                                </div>
                            </div>

                            <div className="post-content">
                                <p>{post.content_text}</p>
                                {post.image_urls && post.image_urls.length > 0 && (
                                    <div className="post-images">
                                        {post.image_urls.map((url, idx) => (
                                            <img
                                                key={idx}
                                                src={url}
                                                alt={`Post image ${idx + 1}`}
                                                className="post-image"
                                                onError={(e) => {
                                                    e.target.style.display = 'none';
                                                }}
                                            />
                                        ))}
                                    </div>
                                )}
                            </div>

                            <div className="post-footer">
                                <button
                                    className="action-btn"
                                    onClick={() => handleLike(post.id)}
                                >
                                    ❤️ {post.like_count} Likes
                                </button>
                                <button
                                    className="action-btn"
                                    onClick={() => toggleComments(post.id)}
                                >
                                    💬 {post.comment_count} Comments
                                </button>
                            </div>

                            {expandedComments[post.id] && (
                                <div className="comments-section">
                                    <div className="comments-list">
                                        {comments[post.id]?.map(comment => (
                                            <div key={comment.id} className="comment">
                                                <div className="comment-avatar">
                                                    {comment.author_avatar_url ? (
                                                        <img
                                                            src={`${comment.author_avatar_url}?t=${Date.now()}`}
                                                            alt={comment.author_name}
                                                            className="avatar-small"
                                                        />
                                                    ) : (
                                                        <div className="avatar-placeholder-small">
                                                            {comment.author_name?.[0]?.toUpperCase() || 'U'}
                                                        </div>
                                                    )}
                                                </div>
                                                <div className="comment-content">
                                                    <div className="comment-author-name">
                                                        {comment.author_name || `User #${comment.user_id}`}
                                                    </div>
                                                    <div className="comment-text">
                                                        {comment.comment_text}
                                                    </div>
                                                    <div className="comment-time">
                                                        {new Date(comment.created_at).toLocaleString()}
                                                    </div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                    <div className="add-comment">
                                        <input
                                            type="text"
                                            className="input"
                                            placeholder="Write a comment..."
                                            value={newComment[post.id] || ''}
                                            onChange={(e) => setNewComment({
                                                ...newComment,
                                                [post.id]: e.target.value
                                            })}
                                            onKeyPress={(e) => {
                                                if (e.key === 'Enter') {
                                                    handleAddComment(post.id);
                                                }
                                            }}
                                        />
                                        <button
                                            className="btn btn-sm btn-primary"
                                            onClick={() => handleAddComment(post.id)}
                                        >
                                            Send
                                        </button>
                                    </div>
                                </div>
                            )}
                        </div>
                    ))}

                    {posts.length === 0 && (
                        <div className="empty-state">
                            <p>No posts yet. Be the first to share!</p>
                        </div>
                    )}
                </div>
            )}

            {/* Profile Modal */}
            {showProfileModal && selectedProfile && (
                <div className="profile-modal-overlay" onClick={() => setShowProfileModal(false)}>
                    <div className="profile-modal" onClick={(e) => e.stopPropagation()}>
                        {selectedProfile.avatar_url ? (
                            <img
                                src={`${selectedProfile.avatar_url}?t=${Date.now()}`}
                                alt={selectedProfile.display_name}
                                className="profile-modal-avatar"
                            />
                        ) : (
                            <div className="avatar-placeholder avatar-xl" style={{ margin: '0 auto 20px' }}>
                                {selectedProfile.display_name?.[0]?.toUpperCase() || 'U'}
                            </div>
                        )}
                        <h2 className="profile-modal-name">{selectedProfile.display_name || 'User'}</h2>
                        {selectedProfile.bio && <p className="profile-modal-bio">{selectedProfile.bio}</p>}
                        {selectedProfile.age && <p><strong>Age:</strong> {selectedProfile.age}</p>}
                        {selectedProfile.location && <p><strong>Location:</strong> {selectedProfile.location}</p>}
                        {selectedProfile.interests && selectedProfile.interests.length > 0 && (
                            <div style={{ marginTop: '15px' }}>
                                <strong>Interests:</strong>
                                <div style={{ marginTop: '8px', display: 'flex', flexWrap: 'wrap', gap: '8px', justifyContent: 'center' }}>
                                    {selectedProfile.interests.map((interest, i) => (
                                        <span key={i} className="tag tag-pink">{interest}</span>
                                    ))}
                                </div>
                            </div>
                        )}
                        <div className="profile-modal-actions">
                            {user && user.id !== selectedProfile.user_id && (
                                <button
                                    className="btn btn-primary"
                                    onClick={() => handleConnect(selectedProfile.user_id)}
                                >
                                    💕 Request a Date
                                </button>
                            )}
                            <button
                                className="btn btn-secondary"
                                onClick={() => setShowProfileModal(false)}
                            >
                                Close
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default SquarePage;

