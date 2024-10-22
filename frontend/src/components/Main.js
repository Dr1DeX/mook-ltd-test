import React from 'react';
import { Container, Box } from '@mui/material';

import Chat from './Chat';

const Main = () => {
    return (
        <Container maxWidth='lg'>
            <Box mt={2} mb={2}>
                <Chat />
            </Box>
        </Container>
    )
}

export default Main;