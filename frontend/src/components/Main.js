import React, { useState, useEffect, useRef } from 'react';
import io from 'socket.io-client';
import { Box, TextField, IconButton, Typography, Container, Paper, List, ListItem, ListItemText } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import Cookies from 'js-cookie';
import {jwtDecode} from 'jwt-decode';

const Main = () => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]); 
  const messageEndRef = useRef(null);
  const socket = useRef(null);
  const token = Cookies.get('token');

  const getUserIdFromToken = () => {
    if (!token) return null;
    try {
      const decodedToken = jwtDecode(token);
      return decodedToken.user_id;
    } catch (error) {
      return null;
    }
  };

  useEffect(() => {
    socket.current = io('ws://localhost:8000');

    socket.current.emit('request_history');

    socket.current.on('chat_history', (history) => {
      setMessages(history);
    });

    // Обработчик для получения новых сообщений
    socket.current.on('message', (newMessage) => {
      setMessages((prevMessages) => [...prevMessages, newMessage]);
    });

    return () => {
      if (socket.current) {
        socket.current.disconnect();
      }
    };
  }, []);

  const sendMessage = () => {
    if (message.trim()) {
      const userId = getUserIdFromToken();
      const newMessage = { text: message, sender_id: userId };
      socket.current.emit('message', newMessage);
      setMessage('');
    }
  };

  const scrollToBottom = () => {
    if (messageEndRef.current) {
      messageEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  useEffect(() => {
    scrollToBottom(); // Прокрутка вниз при добавлении нового сообщения
  }, [messages]);

  return (
    <Container maxWidth='md' sx={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <Typography variant='h4' align='center' gutterBottom>
        MegaChat
      </Typography>
      <Paper sx={{ flexGrow: 1, overflow: 'auto', p: 2, mb: 2 }}>
        <List>
          {messages.map((msg, index) => (
            <ListItem key={index}>
              <ListItemText primary={msg.text} />
            </ListItem>
          ))}
          <div ref={messageEndRef} />
        </List>
      </Paper>
      <Box component="form" sx={{ display: 'flex' }}>
        <TextField
          fullWidth
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Введите сообщение..."
        />
        <IconButton color="primary" onClick={sendMessage}>
          <SendIcon />
        </IconButton>
      </Box>
    </Container>
  );
};

export default Main;
