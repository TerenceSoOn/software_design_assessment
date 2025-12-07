/**
 * Datemate service - datemate connections.
 */
import api from './api';

export const datemateService = {
    /**
     * Send a datemate connection request.
     */
    async sendRequest(userId) {
        const response = await api.post('/datemates/', { receiver_id: userId });
        return response.data;
    },

    /**
     * Check connection status with a specific user.
     */
    async checkConnectionStatus(userId) {
        try {
            const [myConnections, pendingRequests, sentRequests] = await Promise.all([
                api.get('/datemates/').then(r => r.data),
                api.get('/datemates/pending').then(r => r.data),
                api.get('/datemates/sent').then(r => r.data)
            ]);

            const isDatemate = myConnections.some(c => c.receiver_id === userId || c.requester_id === userId);
            const isPendingIncoming = pendingRequests.some(c => c.requester_id === userId);
            const isPendingOutgoing = sentRequests.some(c => c.receiver_id === userId);

            let status = 'none';
            if (isDatemate) status = 'connected';
            else if (isPendingIncoming) status = 'pending_incoming';
            else if (isPendingOutgoing) status = 'pending_outgoing';

            return {
                isConnected: isDatemate,
                isPending: isPendingIncoming || isPendingOutgoing,
                status
            };
        } catch (error) {
            console.error("Failed to check connection status", error);
            return { isConnected: false, isPending: false, status: 'error' };
        }
    },
    /**
     * Get all accepted connections (datemates).
     */
    async getDatemates() {
        const response = await api.get('/datemates/');
        return response.data;
    },

    /**
     * Get pending connection requests.
     */
    async getPendingRequests() {
        const response = await api.get('/datemates/pending');
        return response.data;
    },

    /**
     * Accept a connection request.
     */
    async acceptRequest(connectionId) {
        const response = await api.post(`/datemates/accept/${connectionId}`);
        return response.data;
    },

    /**
     * Reject a connection request.
     */
    async rejectRequest(connectionId) {
        const response = await api.post(`/datemates/reject/${connectionId}`);
        return response.data;
    },
};

export default datemateService;
