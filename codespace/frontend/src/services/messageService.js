/**
 * Message service - private messaging between datemates.
 */
import api from './api';

export const messageService = {
    /**
     * Get conversation with a specific user.
     */
    async getConversation(userId) {
        const response = await api.get(`/messages/${userId}`);
        return response.data;
    },

    /**
     * Send a private message.
     * @param {number} receiverId - Receiver user ID
     * @param {string} content - Message text content
     * @param {string|null} imageUrl - Optional image URL
     */
    async sendMessage(receiverId, content, imageUrl = null) {
        const response = await api.post(`/messages/${receiverId}`, {
            content: content || "",
            image_url: imageUrl
        });
        return response.data;
    },

    /**
     * Upload an image and return the URL.
     * @param {File} file - Image file to upload
     */
    async uploadImage(file) {
        const formData = new FormData();
        formData.append('file', file);
        const response = await api.post('/upload/image', formData);
        return response.data; // { url: "..." }
    },

    /**
     * Mark a specific message as read.
     */
    async markAsRead(messageId) {
        const response = await api.put(`/messages/${messageId}/read`);
        return response.data;
    }
};

export default messageService;
