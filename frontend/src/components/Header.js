import React, { useState } from 'react';
import { AppBar, Toolbar, Typography, Button, IconButton, useMediaQuery, Drawer, List, ListItem, ListItemText, CircularProgress, Box } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import apiClient from '../apiClient';
import "react-toastify/dist/ReactToastify.css";
import { toast } from 'react-toastify';

const Header = () => {
    const navigate = useNavigate();
    const isMobile = useMediaQuery('(max-width:600px)');
    const [drawerOpen, setDrawerOpen] = useState(false);
    const [loading, setLoading] = useState(false);

    const handleLogout = async () => {
        const token = Cookies.get('token');
        if (!token) {
            navigate('/login');
            return;
        }

        setLoading(true);

        try {
            const response = await apiClient.post('/auth/logout', { token });
            if (response.status === 200) {
                toast.success('Вы успешно вышли из системы. Приходите ещё!');
                Cookies.remove('token');
                navigate('/login');
            }
        } catch (error) {
            if (error.response || error.response.status === 400) {
                Cookies.remove('token');
                navigate('/login');
            }
        } finally {
            setLoading(false);
        }
    };

    const toggleDrawer = (open) => () => {
        setDrawerOpen(open);
    };

    const token = Cookies.get('token');

    const renderDrawer = () => (
        <Drawer anchor='right' open={drawerOpen} onClose={toggleDrawer(false)}>
            <List>
                {token ? (
                    <ListItem button onClick={handleLogout}>
                        <ListItemText primary='Выйти' />
                    </ListItem>
                ) : (
                    <>
                        <ListItem button onClick={() => { toggleDrawer(false)(); navigate('/login'); }}>
                            <ListItemText primary='Войти' />
                        </ListItem>
                        <ListItem button onClick={() => { toggleDrawer(false)(); navigate('/register'); }}>
                            <ListItemText primary='Регистрация' />
                        </ListItem>
                    </>
                )}
            </List>
        </Drawer>
    );

    return (
        <AppBar position='static'>
            <Toolbar>
                <Typography variant='h6' sx={{ flexGrow: 1 }}>
                    MegaChat
                </Typography>
                {isMobile ? (
                    <IconButton color='inherit' onClick={toggleDrawer(true)}>
                        <MenuIcon />
                    </IconButton>
                ) : (
                    <>
                        {loading ? (
                            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', p: 1 }}>
                                <CircularProgress color='inherit' size={24} />
                            </Box>
                        ) : token ? (
                            <Button color='inherit' onClick={handleLogout}>
                                Выйти
                            </Button>
                        ) : (
                            <>
                                <Button color='inherit' onClick={() => navigate('/login')}>
                                    Войти
                                </Button>
                                <Button color='inherit' onClick={() => navigate('/register')}>
                                    Регистрация
                                </Button>
                            </>
                        )}
                    </>
                )}
            </Toolbar>
            {renderDrawer()}
        </AppBar>
    );
};

export default Header;