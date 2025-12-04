/**
 * Post service - Public Square posts.
 */
import api from './api';

export const postService = {
    /**
     * Get all posts (feed).
     */
    async getPosts(skip = 0, limit = 20) {
        const response = await api.get(`/posts/?skip=${skip}&limit=${limit}`);
        return response.data;
    },

    /**
     * Create a new post.
     */
    async createPost(postData) {
        const response = await api.post('/posts/', postData);
        return response.data;
    },

    /**
     * Like a post.
     */
    async likePost(postId) {
        const response = await api.post(`/posts/${postId}/like`);
        return response.data;
    },

    /**
     * Unlike a post.
     */
    async unlikePost(postId) {
        await api.delete(`/posts/${postId}/like`);
    },

    /**
     * Get comments for a post.
     */
    async getComments(postId) {
        const response = await api.get(`/posts/${postId}/comments`);
        return response.data;
    },

    /**
     * Add a comment to a post.
     */
    async addComment(postId, commentText) {
        const response = await api.post(`/posts/${postId}/comments`, {
            comment_text: commentText,
        });
        return response.data;
    },
};

export default postService;
