/**
 * Connection service - datemate connections.
 */
import api from './api';

export const connectionService = {
    /**
     * Send a datemate connection request.
     */
    async sendRequest(receiverId) {
        const response = await api.post('/connections/', {
            receiver_id: receiverId,
        });
        return response.data;
    },

    /**
     * Get all accepted connections (datemates).
     */
    async getConnections() {
        const response = await api.get('/connections/');
        return response.data;
    },

    /**
     * Get pending connection requests.
     */
    async getPendingRequests() {
        const response = await api.get('/connections/pending');
        return response.data;
    },

    /**
     * Accept a connection request.
     */
    async acceptRequest(connectionId) {
        const response = await api.put(`/connections/${connectionId}/accept`);
        return response.data;
    },

    /**
     * Reject a connection request.
     */
    async rejectRequest(connectionId) {
        const response = await api.put(`/connections/${connectionId}/reject`);
        return response.data;
    },
};

export default connectionService;
