const API_BASE = '/api';

export const sessionAPI = {
  // Get all sessions
  getSessions: async () => {
    const response = await fetch(`${API_BASE}/session-manager/sessions`);
    if (!response.ok) throw new Error(`Failed to fetch sessions: ${response.status}`);
    return response.json();
  },

  // Get a single session
  getSession: async (sessionId) => {
    const response = await fetch(`${API_BASE}/session-manager/sessions/${sessionId}`);
    if (!response.ok) throw new Error(`Failed to fetch session: ${response.status}`);
    return response.json();
  },

  // Create a session
  createSession: async (name, description = null) => {
    const response = await fetch(`${API_BASE}/session-manager/sessions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name, description }),
    });
    if (!response.ok) throw new Error(`Failed to create session: ${response.status}`);
    return response.json();
  },

  // Update a session
  updateSession: async (sessionId, updates) => {
    const response = await fetch(`${API_BASE}/session-manager/sessions/${sessionId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updates),
    });
    if (!response.ok) throw new Error(`Failed to update session: ${response.status}`);
    return response.json();
  },

  // Delete a session
  deleteSession: async (sessionId) => {
    const response = await fetch(`${API_BASE}/session-manager/sessions/${sessionId}`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error(`Failed to delete session: ${response.status}`);
    return response.status === 204;
  },

  // Get conversation content
  getConversationContent: async (sessionId, conversationId) => {
    const response = await fetch(`${API_BASE}/session-manager/sessions/${sessionId}/conversations/${conversationId}/content`);
    if (!response.ok) throw new Error(`Failed to fetch conversation content: ${response.status}`);
    return response.text();
  },

  // Delete a conversation
  deleteConversation: async (sessionId, conversationId) => {
    const response = await fetch(`${API_BASE}/session-manager/sessions/${sessionId}/conversations/${conversationId}`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error(`Failed to delete conversation: ${response.status}`);
    return response.status === 204;
  },
};

export const ragAPI = {
  // Query RAG with streaming response
  initialQuery: async function* (query, sessionId) {
    const response = await fetch(`${API_BASE}/rag/initial_query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: query,
        session_id: sessionId,
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to query RAG: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        yield chunk;
      }
    } finally {
      reader.releaseLock();
    }
  },
};

export const ttsAPI = {
  // Generate audio from text
  generateAudio: async (text, voice = 'Eva') => {
    const response = await fetch(`${API_BASE}/text_to_speech/generate?text=${encodeURIComponent(text)}&voice=${voice}`, {
      method: 'POST',
    });
    if (!response.ok) throw new Error(`Failed to generate audio: ${response.status}`);
    return response.blob();
  },
};

