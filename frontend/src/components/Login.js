import React, { useState } from 'react';
import { TextField, Button, Container, Typography, Paper, Box, Link, CircularProgress } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import Cookies from 'js-cookie';
import "react-toastify/dist/ReactToastify.css";
import apiClient from '../apiClient';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
    setLoading(true);
    try {
        const response = await new Promise((resolve, reject) => {
            setTimeout(async () => {
                try {
                    const result = await apiClient.post('/auth/login', { email, password });
                    resolve(result);
                } catch (err) {
                    reject(err);
                }
            }, 3000);
        });
        if (response.status === 200) {
            Cookies.set('token', response.data.access_token, { expires: 100 / (60 * 60 * 24) });
            toast.success('Вы успешно авторизовались!');
            navigate('/');
        }
    } catch (error) {
        console.error("Ошибка авторизации: ", error); 
        if (error.response && (error.response.status === 401 || error.response.status === 404)) {
            toast.warning('Неверные имя пользователя или пароль');
        } else {
            toast.error('Произошла ошибка!');
            Cookies.remove('token');
        }
    } finally {
        setLoading(false);
    }
    };

    return (
        <Container maxWidth="xs">
            <Paper elevation={3}>
                <Box p={3}>
                    <Typography variant="h4" textAlign="center" gutterBottom>
                        Авторизация
                    </Typography>
                    <form onSubmit={handleSubmit}>
                        <TextField
                            label="Email"
                            type="email"
                            fullWidth
                            margin="normal"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                        <TextField
                            label="Пароль"
                            type="password"
                            fullWidth
                            margin="normal"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        <Button type="submit" fullWidth variant="contained" color="primary" disabled={loading}>
                            {loading ? <CircularProgress size={24} /> : 'Войти'}
                        </Button>
                    </form>
                    <Box mt={2} textAlign="center">
                        <Link 
                            href="/register" 
                            underline="none" 
                            sx={{ 
                                color: 'primary.main', 
                                transition: 'color 0.3s', 
                                '&:hover': { color: 'secondary.main' } 
                            }}>
                            Нет аккаунта? Зарегистрироваться
                        </Link>
                    </Box>
                </Box>
            </Paper>
        </Container>
    );
};

export default Login;