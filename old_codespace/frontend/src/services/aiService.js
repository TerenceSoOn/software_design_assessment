/**
 * AI service - AI features (Companion, Safety Check).
 */
import api from './api';

export const aiService = {
    /**
     * Chat with AI Companion.
     */
    async chatWithCompanion(message, chatHistory = []) {
        const response = await api.post('/ai/companion', {
            message,
            chat_history: chatHistory,
            scenario: 'companion'
        });
        return response.data;
    },

    /**
     * Practice chat mode.
     */
    async practiceChat(message, chatHistory = [], scenario = 'random_persona') {
        const response = await api.post('/ai/practice', {
            message,
            history: chatHistory, // Note: backend expects 'history' in ChatRequest
            scenario: scenario
        });
        return response.data; // { response: "..." }
    },

    /**
     * Check content safety.
     */
    async checkSafety(message) {
        const response = await api.post('/ai/safety-check', { message });
        return response.data;
    },

    /**
     * Optimize profile bio.
     */
    async optimizeProfile(currentBio) {
        const response = await api.post('/ai/optimize-profile', { current_bio: currentBio });
        return response.data;
    },

    /**
     * Get wingman analysis and suggestions.
     * Returns { analysis: string, suggestions: string[] }
     */
    async getWingmanSuggestions(partnerProfile, chatHistory = []) {
        const response = await api.post('/ai/wingman', {
            partner_profile: JSON.stringify(partnerProfile),
            chat_history: chatHistory
        });
        // Backend now returns { analysis: "...", suggestions: [...] }
        return response.data;
    },

    /**
     * Analyze chat atmosphere.
     */
    async analyzeAtmosphere(chatHistory) {
        const response = await api.post('/ai/atmosphere', { chat_history: chatHistory });
        return response.data;
    },

    /**
     * Imitate Ex.
     */
    async imitateEx(message, chatHistory = [], exStyleSamples = '', targetUserId = null) {
        const response = await api.post('/ai/miss-ex', {
            message,
            history: chatHistory,
            ex_chat_history: exStyleSamples,
            target_user_id: targetUserId
        });
        return response.data;
    },
};

export default aiService;
