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
     */
    async sendMessage(receiverId, content) {
        const response = await api.post(`/messages/${receiverId}`, {
            content
        });
        return response.data;
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
