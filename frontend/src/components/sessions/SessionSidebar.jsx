import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  CircularProgress,
  Alert,
  IconButton,
  Collapse,
  Card,
  CardContent,
  Avatar,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import DescriptionIcon from '@mui/icons-material/Description';
import PersonIcon from '@mui/icons-material/Person';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import { sessionAPI } from '../../helpers/api';
import DeleteConfirmDialog from './DeleteConfirmDialog';

const SessionSidebar = ({ onSessionSelect, onConversationSelect, selectedSession, selectedConversation, onAddSession, refreshTrigger, onRefresh }) => {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedSessions, setExpandedSessions] = useState({});
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [itemToDelete, setItemToDelete] = useState(null);
  const [deleteType, setDeleteType] = useState(null);

  const loadSessions = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await sessionAPI.getSessions();
      setSessions(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSessions();
  }, []);

  useEffect(() => {
    if (refreshTrigger > 0) {
      loadSessions();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [refreshTrigger]);

  useEffect(() => {
    // Auto-expand selected session
    if (selectedSession) {
      setExpandedSessions(prev => ({ ...prev, [selectedSession.session_id]: true }));
    }
  }, [selectedSession]);

  const handleSessionClick = async (session) => {
    const fullSession = await sessionAPI.getSession(session.session_id);
    onSessionSelect(fullSession);
  };

  const toggleSession = (sessionId, e) => {
    if (e) {
      e.stopPropagation();
    }
    setExpandedSessions(prev => ({
      ...prev,
      [sessionId]: !prev[sessionId],
    }));
  };

  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const handleDeleteSession = (session, e) => {
    e.stopPropagation();
    setItemToDelete(session);
    setDeleteType('session');
    setDeleteDialogOpen(true);
  };

  const handleDeleteConversation = (session, conversation, e) => {
    e.stopPropagation();
    setItemToDelete({ session, conversation });
    setDeleteType('conversation');
    setDeleteDialogOpen(true);
  };

  const confirmDelete = async () => {
    try {
      if (deleteType === 'session') {
        await sessionAPI.deleteSession(itemToDelete.session_id);
        if (selectedSession?.session_id === itemToDelete.session_id) {
          onSessionSelect(null);
          onConversationSelect(null);
        }
      } else if (deleteType === 'conversation') {
        await sessionAPI.deleteConversation(
          itemToDelete.session.session_id,
          itemToDelete.conversation.conversation_id
        );
        if (selectedConversation?.conversation_id === itemToDelete.conversation.conversation_id) {
          onConversationSelect(null);
        }
        // Reload the session to get updated conversations
        const updatedSession = await sessionAPI.getSession(itemToDelete.session.session_id);
        onSessionSelect(updatedSession);
      }
      
      setDeleteDialogOpen(false);
      setItemToDelete(null);
      setDeleteType(null);
      
      // Trigger refresh
      if (onRefresh) {
        onRefresh();
      } else {
        loadSessions();
      }
    } catch (err) {
      setError(err.message);
      setDeleteDialogOpen(false);
    }
  };

  const getDeleteDialogTitle = () => {
    if (deleteType === 'session') {
      return 'Delete Session';
    }
    return 'Delete Conversation';
  };

  const getDeleteDialogMessage = () => {
    if (deleteType === 'session') {
      return `Are you sure you want to delete the session "${itemToDelete?.name}"? This will delete all conversations in this session. This action cannot be undone.`;
    }
    return `Are you sure you want to delete this conversation? This action cannot be undone.`;
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight={400} sx={{ backgroundColor: '#ffffff' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 2, backgroundColor: '#ffffff' }}>
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  return (
    <Box
      sx={{
        width: '100%',
        height: '100%',
        backgroundColor: '#f5f5f5',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
      }}
    >
      <Box sx={{ p: 2, pb: 1, backgroundColor: '#ffffff', borderBottom: '1px solid #e0e0e0' }}>
        <Typography
          variant="h6"
          sx={{
            fontWeight: 600,
            color: '#424242',
            fontSize: '1.1rem',
          }}
        >
          Sessions
        </Typography>
      </Box>
      <Box sx={{ flex: 1, overflow: 'auto', p: 2 }}>
        {sessions.length === 0 ? (
          <Box sx={{ p: 3, textAlign: 'center' }}>
            <Typography sx={{ color: '#666' }}>No sessions found</Typography>
          </Box>
        ) : (
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
            {sessions.map((session) => {
              const isExpanded = expandedSessions[session.session_id];
              const isSelected = selectedSession?.session_id === session.session_id;

              return (
                <Box key={session.session_id}>
                  <Card
                    onClick={() => handleSessionClick(session)}
                    sx={{
                      cursor: 'pointer',
                      backgroundColor: isSelected ? '#e3f2fd' : '#ffffff',
                      borderRadius: 2,
                      boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                      border: isSelected ? '2px solid #1976d2' : '1px solid #e0e0e0',
                      transition: 'all 0.2s',
                      '&:hover': {
                        boxShadow: '0 2px 6px rgba(0,0,0,0.15)',
                        borderColor: isSelected ? '#1976d2' : '#bdbdbd',
                      },
                    }}
                  >
                    <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                      <Box sx={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
                        <Box sx={{ flex: 1, minWidth: 0 }}>
                          <Typography
                            variant="body1"
                            sx={{
                              fontWeight: 500,
                              color: '#424242',
                              mb: 0.5,
                              fontSize: '0.95rem',
                            }}
                          >
                            {session.name}
                          </Typography>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mb: 0.5 }}>
                            <PersonIcon sx={{ fontSize: 14, color: '#757575' }} />
                            <Typography variant="caption" sx={{ color: '#757575', fontSize: '0.75rem' }}>
                              Admin
                            </Typography>
                          </Box>
                        </Box>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5, ml: 1 }}>
                          <IconButton
                            size="small"
                            onClick={(e) => {
                              e.stopPropagation();
                              // Handle add conversation - can be implemented later
                            }}
                            sx={{
                              color: '#757575',
                              '&:hover': { backgroundColor: '#f5f5f5' },
                            }}
                            title="Add conversation"
                          >
                            <AddIcon fontSize="small" />
                          </IconButton>
                          <IconButton
                            size="small"
                            onClick={(e) => toggleSession(session.session_id, e)}
                            sx={{
                              color: '#757575',
                              '&:hover': { backgroundColor: '#f5f5f5' },
                            }}
                          >
                            {isExpanded ? <ExpandLessIcon fontSize="small" /> : <ExpandMoreIcon fontSize="small" />}
                          </IconButton>
                          <IconButton
                            size="small"
                            onClick={(e) => handleDeleteSession(session, e)}
                            sx={{
                              color: '#d32f2f',
                              '&:hover': { backgroundColor: '#ffebee' },
                            }}
                            title="Delete session"
                          >
                            <DeleteIcon fontSize="small" />
                          </IconButton>
                        </Box>
                      </Box>
                    </CardContent>
                  </Card>

                  <Collapse in={isExpanded} timeout="auto" unmountOnExit>
                    <Box sx={{ pr: 2, pt: 0.5, pb: 1 }}>
                      {session.conversations && session.conversations.length > 0 ? (
                        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.75 }}>
                          {session.conversations.map((conversation, idx) => {
                            const isConvSelected = selectedConversation?.conversation_id === conversation.conversation_id;
                            
                            return (
                              <Card
                                key={conversation.conversation_id}
                                onClick={() => onConversationSelect(conversation)}
                                sx={{
                                  cursor: 'pointer',
                                  backgroundColor: isConvSelected ? '#e3f2fd' : '#e3f2fd',
                                  borderRadius: 2,
                                  boxShadow: '0 1px 2px rgba(0,0,0,0.08)',
                                  border: isConvSelected ? '2px solid #1976d2' : '1px solid #90caf9',
                                  borderLeft: isConvSelected ? '3px solid #d32f2f' : '3px solid #d32f2f',
                                  transition: 'all 0.2s',
                                  width: '100%',
                                  '&:hover': {
                                    boxShadow: '0 2px 4px rgba(0,0,0,0.12)',
                                    borderColor: isConvSelected ? '#1976d2' : '#64b5f6',
                                  },
                                }}
                              >
                                <CardContent sx={{ p: 1, py: 0.75, '&:last-child': { pb: 0.75 } }}>
                                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 1 }}>
                                    <Box sx={{ flex: 1, minWidth: 0, display: 'flex', alignItems: 'center', gap: 0.75 }}>
                                      <DescriptionIcon sx={{ fontSize: 16, color: '#1976d2', flexShrink: 0 }} />
                                      <Box sx={{ flex: 1, minWidth: 0 }}>
                                        <Typography
                                          variant="body2"
                                          sx={{
                                            fontWeight: 500,
                                            color: '#424242',
                                            fontSize: '0.8rem',
                                            overflow: 'hidden',
                                            textOverflow: 'ellipsis',
                                            whiteSpace: 'nowrap',
                                            lineHeight: 1.2,
                                          }}
                                        >
                                          {conversation.conversation_id.slice(-8)}
                                        </Typography>
                                        <Typography variant="caption" sx={{ color: '#757575', fontSize: '0.65rem', lineHeight: 1.2 }}>
                                          {formatDate(conversation.added_at).split(' ')[0]}
                                        </Typography>
                                      </Box>
                                    </Box>
                                    <IconButton
                                      size="small"
                                      onClick={(e) => handleDeleteConversation(session, conversation, e)}
                                      sx={{
                                        color: '#d32f2f',
                                        padding: 0.5,
                                        '&:hover': { backgroundColor: '#ffebee' },
                                      }}
                                      title="Delete conversation"
                                    >
                                      <DeleteIcon sx={{ fontSize: 16 }} />
                                    </IconButton>
                                  </Box>
                                </CardContent>
                              </Card>
                            );
                          })}
                        </Box>
                      ) : (
                        <Box sx={{ pl: 2, py: 1 }}>
                          <Typography variant="caption" sx={{ color: '#999', fontSize: '0.75rem' }}>
                            No conversations
                          </Typography>
                        </Box>
                      )}
                    </Box>
                  </Collapse>
                </Box>
              );
            })}
          </Box>
        )}
      </Box>

      <Box sx={{ p: 2, borderTop: '1px solid #e0e0e0', backgroundColor: '#ffffff' }}>
        <Box
          onClick={onAddSession}
          sx={{
            backgroundColor: '#1976d2',
            color: '#ffffff',
            width: '100%',
            height: 48,
            borderRadius: 2,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: 1,
            cursor: 'pointer',
            transition: 'background-color 0.2s',
            '&:hover': {
              backgroundColor: '#1565c0',
            },
          }}
        >
          <AddIcon />
          <Typography sx={{ fontWeight: 500, fontSize: '0.9rem' }}>
            Add session
          </Typography>
        </Box>
      </Box>

      <DeleteConfirmDialog
        open={deleteDialogOpen}
        onClose={() => {
          setDeleteDialogOpen(false);
          setItemToDelete(null);
          setDeleteType(null);
        }}
        onConfirm={confirmDelete}
        title={getDeleteDialogTitle()}
        message={getDeleteDialogMessage()}
        itemName={deleteType === 'session' ? itemToDelete?.name : 'conversation'}
      />
    </Box>
  );
};

export default SessionSidebar;
