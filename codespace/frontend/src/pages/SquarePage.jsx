/**
 * Square Page - Public posts feed.
 */
import { useState, useEffect } from 'react';
import { postService } from '../services/postService';
import { useAuth } from '../context/AuthContext';
import './SquarePage.css';

function SquarePage() {
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [newPostContent, setNewPostContent] = useState('');
    const { user } = useAuth();

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

        try {
            const newPost = await postService.createPost({
                content_text: newPostContent,
                image_urls: [],
                tags: []
            });
            setPosts([newPost, ...posts]);
            setNewPostContent('');
        } catch (error) {
            console.error('Failed to create post:', error);
            alert('Failed to create post');
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

    return (
        <div className="container square-page">
            <div className="feed-container">
                <div className="create-post-card card">
                    <h3>Share your thoughts</h3>
                    <form onSubmit={handleCreatePost}>
                        <textarea
                            className="input textarea"
                            placeholder="What's on your mind?"
                            value={newPostContent}
                            onChange={(e) => setNewPostContent(e.target.value)}
                            rows="3"
                        />
                        <div className="post-actions">
                            <button
                                type="submit"
                                className="btn btn-primary"
                                disabled={!newPostContent.trim()}
                            >
                                Post
                            </button>
                        </div>
                    </form>
                </div>

                {loading ? (
                    <div className="loading">Loading posts...</div>
                ) : (
                    <div className="posts-list">
                        {posts.map(post => (
                            <div key={post.id} className="post-card card">
                                <div className="post-header">
                                    <div className="post-avatar">
                                        {/* Placeholder avatar */}
                                        U
                                    </div>
                                    <div className="post-meta">
                                        <span className="post-author">User #{post.user_id}</span>
                                        <span className="post-time">
                                            {new Date(post.created_at).toLocaleDateString()}
                                        </span>
                                    </div>
                                </div>

                                <div className="post-content">
                                    <p>{post.content_text}</p>
                                </div>

                                <div className="post-footer">
                                    <button
                                        className="action-btn"
                                        onClick={() => handleLike(post.id)}
                                    >
                                        ❤️ {post.like_count} Likes
                                    </button>
                                    <button className="action-btn">
                                        💬 {post.comment_count} Comments
                                    </button>
                                </div>
                            </div>
                        ))}

                        {posts.length === 0 && (
                            <div className="empty-state">
                                <p>No posts yet. Be the first to share!</p>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}

export default SquarePage;
