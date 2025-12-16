/**
 * Register Page Component
 */
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { authService } from '../services/authService';
import './RegisterPage.css';

function RegisterPage() {
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        confirmPassword: '',
        gender: '',
        preferred_gender: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        // Validation
        if (formData.password !== formData.confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        if (formData.password.length < 6) {
            setError('Password must be at least 6 characters');
            return;
        }

        if (!formData.gender || !formData.preferred_gender) {
            setError('Please select your gender and preference');
            return;
        }

        setLoading(true);

        try {
            console.log('开始注册，发送数据:', {
                username: formData.username,
                password: '***',
                gender: formData.gender,
                preferred_gender: formData.preferred_gender
            });
            
            const registerResult = await authService.register({
                username: formData.username,
                password: formData.password,
                gender: formData.gender,
                preferred_gender: formData.preferred_gender
            });
            
            console.log('注册成功:', registerResult);

            // Auto login after registration
            console.log('开始自动登录...');
            await login(formData.username, formData.password);
            console.log('登录成功，跳转首页');
            navigate('/');
        } catch (err) {
            console.error('Registration error - 完整错误信息:', err);
            console.error('错误类型:', err.constructor.name);
            console.error('错误消息:', err.message);
            console.error('错误响应:', err.response);
            console.error('错误请求配置:', err.config);
            
            // 更详细的错误信息
            let errorMessage = 'Registration failed. Please try again.';
            if (err.response) {
                // 服务器返回了响应
                errorMessage = err.response.data?.detail || err.response.statusText || `Server error: ${err.response.status}`;
            } else if (err.request) {
                // 请求已发送但没有收到响应
                errorMessage = 'Network error: No response from server. Please check if backend is running.';
            } else {
                // 请求配置出错
                errorMessage = err.message || 'Request setup error';
            }
            
            setError(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="register-page">
            <div className="register-container">
                <div className="register-card">
                    <h1>Join FlirtNet</h1>
                    <p className="subtitle">Create your account</p>

                    <form onSubmit={handleSubmit}>
                        <div className="form-group">
                            <input
                                type="text"
                                name="username"
                                className="input"
                                placeholder="Username"
                                value={formData.username}
                                onChange={handleChange}
                                required
                            />
                        </div>

                        <div className="form-row">
                            <div className="form-group">
                                <select
                                    name="gender"
                                    className="form-select"
                                    value={formData.gender}
                                    onChange={handleChange}
                                    required
                                >
                                    <option value="">I am a...</option>
                                    <option value="male">Male</option>
                                    <option value="female">Female</option>
                                    <option value="other">Other</option>
                                </select>
                            </div>
                            <div className="form-group">
                                <select
                                    name="preferred_gender"
                                    className="form-select"
                                    value={formData.preferred_gender}
                                    onChange={handleChange}
                                    required
                                >
                                    <option value="">Looking for...</option>
                                    <option value="male">Male</option>
                                    <option value="female">Female</option>
                                    <option value="any">Any</option>
                                </select>
                            </div>
                        </div>

                        <div className="form-group">
                            <input
                                type="password"
                                name="password"
                                className="input"
                                placeholder="Password"
                                value={formData.password}
                                onChange={handleChange}
                                required
                            />
                        </div>

                        <div className="form-group">
                            <input
                                type="password"
                                name="confirmPassword"
                                className="input"
                                placeholder="Confirm Password"
                                value={formData.confirmPassword}
                                onChange={handleChange}
                                required
                            />
                        </div>

                        {error && <div className="error">{error}</div>}

                        <button type="submit" className="btn btn-primary btn-full" disabled={loading}>
                            {loading ? 'Creating Account...' : 'Register'}
                        </button>
                    </form>

                    <p className="login-link">
                        Already have an account? <Link to="/login">Login here</Link>
                    </p>
                </div>
            </div>
        </div>
    );
}

export default RegisterPage;
