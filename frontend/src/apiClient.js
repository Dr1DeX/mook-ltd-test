import axios from 'axios';
import Cookies from 'js-cookie';
import config from './config';

const apiClient = axios.create({
    baseURL: `${config.backendUrl}`,
    headers: {
        'Content-Type': 'application/json',
    },
});

apiClient.interceptors.request.use((config) => {
    const token = Cookies.get('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

const refreshAccessToken = async () => {
    try {
        const response = await apiClient.post('/auth/refresh');
        const newToken = response.data.access_token;
        Cookies.set('token', newToken, { expires: 100 / (60 * 60 * 24) }); // 100 секунд
        return newToken;
    } catch (error) {
        console.error('Failed to refresh token: ', error);
        Cookies.remove('token'); // Удаляем токен, если обновление не удалось
        window.location.href = '/login'; // Перенаправляем на страницу логина
        throw error;
    }
};

apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            const newToken = await refreshAccessToken();
            apiClient.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
            return apiClient(originalRequest);
        }
        return Promise.reject(error);
    }
);

export default apiClient;
