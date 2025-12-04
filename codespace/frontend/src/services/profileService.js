/**
 * Profile service - user profile operations.
 */
import api from './api';

export const profileService = {
    /**
     * Get current user's profile.
     */
    async getMyProfile() {
        const response = await api.get('/profiles/me');
        return response.data;
    },

    /**
     * Get any user's profile by ID.
     */
    async getProfile(userId) {
        const response = await api.get(`/profiles/${userId}`);
        return response.data;
    },

    /**
     * Update current user's profile.
     */
    async updateProfile(profileData) {
        const response = await api.put('/profiles/me', profileData);
        return response.data;
    },
};

export default profileService;
