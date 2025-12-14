import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  CircularProgress,
} from '@mui/material';
import { sessionAPI } from '../../helpers/api';

const ContentArea = ({ selectedConversation, selectedSession }) => {
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (selectedConversation && selectedSession) {
      loadConversationContent();
    } else {
      setContent('');
    }
  }, [selectedConversation, selectedSession]);

  const loadConversationContent = async () => {
    if (!selectedConversation || !selectedSession) return;

    setLoading(true);
    try {
      const text = await sessionAPI.getConversationContent(selectedSession.session_id, selectedConversation.conversation_id);
      setContent(text);
    } catch (error) {
      setContent('Error loading content: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  if (!selectedConversation) {
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
        <Typography sx={{ color: '#999' }}>Select a conversation to view content</Typography>
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
      }}
    >
      <Box sx={{ p: 2, borderBottom: '1px solid #e0e0e0' }}>
        <Typography variant="h6">
          Titre
        </Typography>
      </Box>

      <Box sx={{ flex: 1, overflow: 'auto', p: 3, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        {loading ? (
          <Box display="flex" justifyContent="center" alignItems="center" minHeight={200}>
            <CircularProgress />
          </Box>
        ) : (
          <Typography
            sx={{
              whiteSpace: 'pre-wrap',
              color: '#424242',
              lineHeight: 1.6,
              fontFamily: 'monospace',
              fontSize: '0.9rem',
              textAlign: 'center',
            }}
          >
            {content ? `"""${content}"""` : 'No content available'}
          </Typography>
        )}
      </Box>
    </Box>
  );
};

export default ContentArea;

