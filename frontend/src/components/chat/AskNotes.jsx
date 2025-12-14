import { useState } from 'react';
import {
  Box,
  Typography,
  TextField,
  IconButton,
  Paper,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

const AskNotes = ({ selectedSession }) => {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);

  const handleSend = async () => {
    if (!query.trim() || !selectedSession) return;

    const userMessage = { type: 'user', text: query };
    setMessages(prev => [...prev, userMessage]);
    setQuery('');

    // TODO: Implement RAG request to backend
    // For now, just add a placeholder response
    setTimeout(() => {
      const botMessage = { type: 'bot', text: 'This is a placeholder response. RAG functionality will be implemented here.' };
      setMessages(prev => [...prev, botMessage]);
    }, 500);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (!selectedSession) {
    return (
      <Box
        sx={{
          width: '100%',
          height: '100%',
          backgroundColor: '#ffffff',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <Typography sx={{ color: '#999' }}>Select a session to ask questions</Typography>
      </Box>
    );
  }

  return (
    <Box
      sx={{
        width: '100%',
        height: '100%',
        backgroundColor: '#ffffff',
        display: 'flex',
        flexDirection: 'column',
        borderLeft: '1px solid #e0e0e0',
      }}
    >
      <Box sx={{ p: 2, borderBottom: '1px solid #e0e0e0' }}>
        <Typography variant="h6">Ask your notes</Typography>
      </Box>

      <Box sx={{ flex: 1, overflow: 'auto', p: 2 }}>
        {messages.length === 0 ? (
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              height: '100%',
            }}
          >
            <Typography sx={{ color: '#999' }}>Start a conversation</Typography>
          </Box>
        ) : (
          <Box>
            {messages.map((message, index) => (
              <Box
                key={index}
                sx={{
                  mb: 2,
                  display: 'flex',
                  justifyContent: message.type === 'user' ? 'flex-end' : 'flex-start',
                }}
              >
                <Paper
                  sx={{
                    p: 2,
                    maxWidth: '80%',
                    backgroundColor: message.type === 'user' ? '#1976d2' : '#f5f5f5',
                    color: message.type === 'user' ? '#ffffff' : '#333',
                  }}
                >
                  <Typography>{message.text}</Typography>
                </Paper>
              </Box>
            ))}
          </Box>
        )}
      </Box>

      <Box sx={{ p: 2, borderTop: '1px solid #e0e0e0' }}>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <TextField
            fullWidth
            placeholder="Type your question..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            size="small"
            sx={{
              '& .MuiOutlinedInput-root': {
                backgroundColor: '#f5f5f5',
              },
            }}
          />
          <IconButton
            onClick={handleSend}
            disabled={!query.trim()}
            sx={{
              backgroundColor: '#1976d2',
              color: '#ffffff',
              '&:hover': {
                backgroundColor: '#1565c0',
              },
              '&:disabled': {
                backgroundColor: '#e0e0e0',
              },
            }}
          >
            <SendIcon />
          </IconButton>
        </Box>
      </Box>
    </Box>
  );
};

export default AskNotes;

