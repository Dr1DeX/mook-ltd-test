import React, { useState, useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import { CircularProgress, Backdrop } from '@mui/material';

const ProtectedRoute = ({ children }) => {
    const [loading, setLoading] = useState(true);
    const token = Cookies.get('token');

    useEffect(() => {
        const timeout = setTimeout(() => {
            setLoading(false);
        }, 2000);

        return () => clearTimeout(timeout);
    }, []);

    if (!token && !loading) {
        return <Navigate to="/login" replace />;
    }

    return (
        <>
            {loading && (
                <Backdrop
                    sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
                    open={loading}
                >
                    <CircularProgress size={80} />
                </Backdrop>
            )}
            {children}
        </>
    );
};

export default ProtectedRoute;