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

    /**
     * Upload user avatar.
     */
    async uploadAvatar(file) {
        const formData = new FormData();
        formData.append('file', file);
        // Assuming the upload endpoint is mounted at /upload/image
        // We need to use 'Content-Type': 'multipart/form-data' which axios handles automatically with FormData
        const response = await api.post('/upload/image', formData);
        return response.data; // Expected { url: "..." }
    },
};

export default profileService;
