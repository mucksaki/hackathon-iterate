import { useState } from 'react';
import {
  Box,
  Typography,
  TextField,
  IconButton,
  Paper,
  CircularProgress,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { ragAPI } from '../../helpers/api';

const AskNotes = ({ selectedSession }) => {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!query.trim() || !selectedSession) return;

    const userMessage = { type: 'user', text: query };
    setMessages(prev => [...prev, userMessage]);
    const currentQuery = query;
    setQuery('');
    setLoading(true);

    // Add empty bot message that will be updated with streaming response
    const botMessageId = Date.now();
    setMessages(prev => [...prev, { id: botMessageId, type: 'bot', text: '' }]);

    try {
      // Stream the response from RAG
      let fullResponse = '';
      for await (const chunk of ragAPI.initialQuery(currentQuery, selectedSession.session_id)) {
        fullResponse += chunk;
        // Update the bot message with accumulated response
        setMessages(prev => prev.map(msg => 
          msg.id === botMessageId ? { ...msg, text: fullResponse } : msg
        ));
      }
    } catch (error) {
      console.error('Error querying RAG:', error);
      setMessages(prev => prev.map(msg => 
        msg.id === botMessageId ? { ...msg, text: `Error: ${error.message}` } : msg
      ));
    } finally {
      setLoading(false);
    }
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
                key={message.id || index}
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
                    whiteSpace: 'pre-wrap',
                  }}
                >
                  {message.text ? (
                    <Typography>{message.text}</Typography>
                  ) : (
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <CircularProgress size={16} />
                      <Typography variant="caption">Thinking...</Typography>
                    </Box>
                  )}
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
            disabled={!query.trim() || loading}
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


