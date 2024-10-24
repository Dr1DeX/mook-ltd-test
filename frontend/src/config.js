const config = {
    backendUrl: process.env.REACT_APP_BACKEND_URL  || 'http://localhost:8000/api/v1',
    wsUrl: process.env.REACT_APP_WS_URL || 'http://localhost:8000/ws'
};

export default config;