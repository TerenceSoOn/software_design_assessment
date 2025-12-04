/**
 * AI service - AI features (Companion, Safety Check).
 */
import api from './api';

export const aiService = {
    /**
     * Chat with AI Companion.
     */
    async chatWithCompanion(messages) {
        const response = await api.post('/ai/companion', { messages });
        return response.data;
    },

    /**
     * Check content safety.
     */
    async checkSafety(text) {
        const response = await api.post('/ai/safety-check', { text });
        return response.data;
    },
};

export default aiService;
