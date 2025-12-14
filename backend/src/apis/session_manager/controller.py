from fastapi import HTTPException
from .service import SessionService
from .models import Session, SessionCreate, SessionUpdate, Conversation, ConversationCreate
from ...commons.router import make_router


@make_router()
def controller(router, session_service: SessionService) -> None:
    @router.post("/sessions", response_model=Session, status_code=201)
    def create_session(session_data: SessionCreate):
        """Create a new session."""
        try:
            session = session_service.create_session(session_data)
            return session
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")
    
    @router.get("/sessions", response_model=list[Session])
    def list_sessions():
        """List all sessions."""
        try:
            sessions = session_service.list_sessions()
            return sessions
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to list sessions: {str(e)}")
    
    @router.get("/sessions/{session_id}", response_model=Session)
    def get_session(session_id: str):
        """Get a session by ID."""
        session = session_service.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session
    
    @router.put("/sessions/{session_id}", response_model=Session)
    def update_session(session_id: str, update_data: SessionUpdate):
        """Update a session."""
        session = session_service.update_session(session_id, update_data)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session
    
    @router.delete("/sessions/{session_id}", status_code=204)
    def delete_session(session_id: str):
        """Delete a session (hard delete)."""
        success = session_service.delete_session(session_id)
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")
        return None
    
    @router.delete("/sessions", status_code=200)
    def delete_all_sessions():
        """Delete all sessions (hard delete)."""
        try:
            deleted_count = session_service.delete_all_sessions()
            return {"message": f"Deleted {deleted_count} session(s)"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete all sessions: {str(e)}")
    
    @router.post("/sessions/{session_id}/conversations", response_model=Conversation, status_code=201)
    def add_conversation(session_id: str, conversation_data: ConversationCreate):
        """Add a conversation to a session."""
        conversation = session_service.add_conversation(session_id, conversation_data.text)
        if not conversation:
            raise HTTPException(status_code=404, detail="Session not found")
        return conversation
    
    @router.get("/sessions/{session_id}/conversations/{conversation_id}", response_model=Conversation)
    def get_conversation(session_id: str, conversation_id: str):
        """Get a specific conversation from a session."""
        conversation = session_service.get_conversation(session_id, conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return conversation
