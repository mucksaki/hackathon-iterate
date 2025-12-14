import { useState, useRef } from 'react';
import {
  Box,
  Typography,
  TextField,
  IconButton,
  Paper,
  CircularProgress,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import VolumeUpIcon from '@mui/icons-material/VolumeUp';
import { ragAPI, ttsAPI } from '../../helpers/api';

const AskNotes = ({ selectedSession }) => {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [playingAudio, setPlayingAudio] = useState(false);
  const audioRef = useRef(null);

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
      
      // Generate and play audio for the complete response
      if (fullResponse.trim()) {
        try {
          setPlayingAudio(true);
          const audioBlob = await ttsAPI.generateAudio(fullResponse);
          const audioUrl = URL.createObjectURL(audioBlob);
          
          if (audioRef.current) {
            audioRef.current.pause();
          }
          
          const audio = new Audio(audioUrl);
          audioRef.current = audio;
          
          audio.onended = () => {
            setPlayingAudio(false);
            URL.revokeObjectURL(audioUrl);
          };
          
          audio.onerror = () => {
            setPlayingAudio(false);
            URL.revokeObjectURL(audioUrl);
          };
          
          await audio.play();
        } catch (audioError) {
          console.error('Error playing audio:', audioError);
          setPlayingAudio(false);
        }
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
                  <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1 }}>
                    {message.text ? (
                      <Typography sx={{ flex: 1 }}>{message.text}</Typography>
                    ) : (
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flex: 1 }}>
                        <CircularProgress size={16} />
                        <Typography variant="caption">Thinking...</Typography>
                      </Box>
                    )}
                    {message.type === 'bot' && message.text && (
                      <IconButton
                        size="small"
                        onClick={async () => {
                          try {
                            setPlayingAudio(true);
                            const audioBlob = await ttsAPI.generateAudio(message.text);
                            const audioUrl = URL.createObjectURL(audioBlob);
                            
                            if (audioRef.current) {
                              audioRef.current.pause();
                            }
                            
                            const audio = new Audio(audioUrl);
                            audioRef.current = audio;
                            
                            audio.onended = () => {
                              setPlayingAudio(false);
                              URL.revokeObjectURL(audioUrl);
                            };
                            
                            audio.onerror = () => {
                              setPlayingAudio(false);
                              URL.revokeObjectURL(audioUrl);
                            };
                            
                            await audio.play();
                          } catch (error) {
                            console.error('Error playing audio:', error);
                            setPlayingAudio(false);
                          }
                        }}
                        disabled={playingAudio}
                        sx={{ 
                          color: playingAudio ? '#1976d2' : '#666',
                          '&:hover': { backgroundColor: 'rgba(0,0,0,0.04)' },
                          mt: -0.5,
                        }}
                        title="Play audio"
                      >
                        <VolumeUpIcon fontSize="small" />
                      </IconButton>
                    )}
                  </Box>
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


