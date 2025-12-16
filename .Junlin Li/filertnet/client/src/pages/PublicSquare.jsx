import { useState } from "react";
import { Link } from "react-router-dom";
import "./PublicSquare.css";

function PublicSquare() {
  // Mock data for posts
  const [posts, setPosts] = useState([
    {
      id: 1,
      author: "Alice Wonder",
      avatar: "https://via.placeholder.com/40",
      time: "2 hours ago",
      content: "Just finished a great hiking trip! The view was amazing. 🏔️",
      likes: 12,
      comments: 3,
      isLiked: false,
    },
    {
      id: 2,
      author: "Bob Builder",
      avatar: "https://via.placeholder.com/40",
      time: "5 hours ago",
      content: "Anyone want to grab coffee and talk about coding? ☕",
      likes: 8,
      comments: 5,
      isLiked: true,
    },
  ]);

  const [newPostContent, setNewPostContent] = useState("");

  const handlePostSubmit = (e) => {
    e.preventDefault();
    if (!newPostContent.trim()) return;

    const newPost = {
      id: Date.now(),
      author: "Current User", // In real app, get from auth context
      avatar: "https://via.placeholder.com/40",
      time: "Just now",
      content: newPostContent,
      likes: 0,
      comments: 0,
      isLiked: false,
    };

    setPosts([newPost, ...posts]);
    setNewPostContent("");
  };

  const toggleLike = (postId) => {
    setPosts(
      posts.map((post) => {
        if (post.id === postId) {
          return {
            ...post,
            likes: post.isLiked ? post.likes - 1 : post.likes + 1,
            isLiked: !post.isLiked,
          };
        }
        return post;
      })
    );
  };

  return (
    <div className="public-square-container">
      <Link to="/" className="back-link">
        &larr; Back to Home
      </Link>
      <div className="feed-header">
        <h2>Public Square</h2>
      </div>

      {/* Create Post Section */}
      <div className="create-post-card">
        <form onSubmit={handlePostSubmit}>
          <textarea
            placeholder="What's on your mind?"
            value={newPostContent}
            onChange={(e) => setNewPostContent(e.target.value)}
          />
          <div className="create-post-actions">
            <button type="button" className="action-btn">
              📷 Add Image
            </button>
            <button type="submit" className="post-button">
              Post
            </button>
          </div>
        </form>
      </div>

      {/* Posts Feed */}
      <div className="posts-feed">
        {posts.map((post) => (
          <div key={post.id} className="post-card">
            <div className="post-header">
              <img
                src={post.avatar}
                alt={post.author}
                className="post-avatar"
              />
              <div className="post-author-info">
                <h4>{post.author}</h4>
                <p className="post-time">{post.time}</p>
              </div>
            </div>

            <div className="post-content">{post.content}</div>

            <div className="post-actions">
              <button
                className={`action-btn ${post.isLiked ? "liked" : ""}`}
                onClick={() => toggleLike(post.id)}
              >
                {post.isLiked ? "❤️" : "🤍"} {post.likes} Likes
              </button>
              <button className="action-btn">
                💬 {post.comments} Comments
              </button>
              <button className="action-btn">↗️ Share</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default PublicSquare;
