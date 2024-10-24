import React, { useState } from 'react';
import { TextField, Button, Container, Typography, Paper, Box, Link, CircularProgress } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import Cookies from 'js-cookie'
import "react-toastify/dist/ReactToastify.css";
import apiClient from '../apiClient';

const Register = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const response = await new Promise((resolve) => {
                setTimeout(async () => {
                    const result = await apiClient.post('/user', { username, password, email });
                    resolve(result);
                }, 3000);
            });
            if (response.status === 200) {
                Cookies.set('token', response.data.access_token, { expires: 100});
                toast.success('Вы успешно зарегистрировались!');
                navigate('/');
            }
        } catch (error) {
            if (error.response && error.response.status === 400) {
                toast.warning('Такой email уже существует!');
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
                        Регистрация
                    </Typography>
                    <form onSubmit={handleSubmit}>
                        <TextField
                            label="Имя пользователя"
                            type="text"
                            fullWidth
                            margin="normal"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
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
                            {loading ? <CircularProgress size={24} /> : 'Регистрация'}
                        </Button>
                    </form>
                    <Box mt={2} textAlign="center">
                        <Link 
                            href="/login" 
                            underline="none" 
                            sx={{ 
                                color: 'primary.main', 
                                transition: 'color 0.3s', 
                                '&:hover': { color: 'secondary.main' } 
                            }}>
                            Есть аккаунт? Войти
                        </Link>
                    </Box>
                </Box>
            </Paper>
        </Container>
    );
};

export default Register;
