/**
 * Authentication Context - manages user authentication state.
 */
import { createContext, useState, useContext, useEffect } from 'react';
import { authService } from '../services/authService';
import { profileService } from '../services/profileService';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);

    // Load user profile on mount if authenticated
    useEffect(() => {
        const loadUser = async () => {
            if (authService.isAuthenticated()) {
                try {
                    const profileData = await profileService.getMyProfile();
                    setProfile(profileData);
                    setUser({ id: profileData.user_id });
                } catch (error) {
                    console.error('Failed to load user profile:', error);
                    authService.logout();
                }
            }
            setLoading(false);
        };

        loadUser();
    }, []);

    const login = async (username, password) => {
        const data = await authService.login(username, password);
        const profileData = await profileService.getMyProfile();
        setProfile(profileData);
        setUser({ id: profileData.user_id });
        return data;
    };

    const register = async (username, email, password) => {
        const userData = await authService.register(username, email, password);
        return userData;
    };

    const logout = () => {
        authService.logout();
        setUser(null);
        setProfile(null);
    };

    const updateUserProfile = (updatedProfile) => {
        setProfile(updatedProfile);
    };

    const value = {
        user,
        profile,
        loading,
        login,
        register,
        logout,
        updateUserProfile,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider');
    }
    return context;
};

export default AuthContext;
