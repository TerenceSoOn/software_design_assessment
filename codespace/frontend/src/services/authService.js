/**
 * Authentication service - handles login, register, logout.
 */
import api from './api';

export const authService = {
    /**
     * Register a new user account.
     */
    async register(userData) {
        const response = await api.post('/auth/register', userData);
        return response.data;
    },

    /**
     * Login with username and password.
     */
    async login(username, password) {
        const response = await api.post('/auth/login', {
            username,
            password,
        });

        // Save token to localStorage
        if (response.data.access_token) {
            localStorage.setItem('token', response.data.access_token);
        }

        return response.data;
    },

    /**
     * Logout - clear token.
     */
    logout() {
        localStorage.removeItem('token');
    },

    /**
     * Check if user is logged in.
     */
    isAuthenticated() {
        return !!localStorage.getItem('token');
    },
};

export default authService;
