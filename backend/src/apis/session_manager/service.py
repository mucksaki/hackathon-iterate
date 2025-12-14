import json
import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .models import Session, SessionCreate, SessionUpdate, Conversation, SessionsData


class SessionService:
    def __init__(self, base_path: str = None, rag_service=None):
        # Get the directory where this file is located
        if base_path is None:
            self.base_path = Path(__file__).parent
        else:
            self.base_path = Path(base_path)
        
        self.sessions_dir = self.base_path / "sessions"
        self.sessions_json_path = self.base_path / "sessions.json"
        self.rag_service = rag_service
        
        # Create sessions directory if it doesn't exist
        self.sessions_dir.mkdir(exist_ok=True)
        
        # Initialize sessions.json if it doesn't exist
        if not self.sessions_json_path.exists():
            self._save_sessions_data(SessionsData(sessions=[]))
    
    def _load_sessions_data(self) -> SessionsData:
        """Load sessions data from JSON file."""
        if not self.sessions_json_path.exists():
            return SessionsData(sessions=[])
        
        try:
            with open(self.sessions_json_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    # File exists but is empty
                    return SessionsData(sessions=[])
                data = json.loads(content)
                return SessionsData(**data)
        except (json.JSONDecodeError, ValueError) as e:
            # If JSON is invalid, initialize with empty sessions
            return SessionsData(sessions=[])
    
    def _save_sessions_data(self, data: SessionsData) -> None:
        """Save sessions data to JSON file."""
        with open(self.sessions_json_path, 'w', encoding='utf-8') as f:
            json.dump(data.model_dump(), f, indent=2, ensure_ascii=False)
    
    def _generate_session_id(self) -> str:
        """Generate a unique session ID."""
        return str(uuid.uuid4())
    
    def _generate_conversation_id(self) -> str:
        """Generate a unique conversation ID."""
        return f"conv-{uuid.uuid4().hex[:8]}"
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.utcnow().isoformat() + "Z"
    
    def create_session(self, session_data: SessionCreate) -> Session:
        """Create a new session."""
        session_id = self._generate_session_id()
        timestamp = self._get_current_timestamp()
        
        # Create session directory
        session_dir = self.sessions_dir / session_id
        session_dir.mkdir(exist_ok=True)
        
        # Store relative paths (relative to session_manager directory)
        conversations_dir_rel = f"sessions/{session_id}/conversations"
        
        # Create conversations subdirectory (using absolute path for file operations)
        conversations_dir_abs = session_dir / "conversations"
        conversations_dir_abs.mkdir(exist_ok=True)
        
        # Create session in RAG service if available (using same UUID)
        if self.rag_service:
            try:
                import asyncio
                from ..rag import schemas as rag_schemas
                # Create RAG session with the same UUID
                rag_session_data = rag_schemas.SessionCreate(
                    session_name=session_data.name,
                    session_description=session_data.description,
                    session_id=session_id  # Pass the same UUID
                )
                # Run async function - use asyncio.run() which creates a new event loop
                # This is safe to use in sync code
                asyncio.run(self.rag_service.create_session(rag_session_data))
                print(f"Successfully created RAG session with ID: {session_id}")
            except Exception as e:
                print(f"Error: Failed to create RAG session: {e}")
                import traceback
                traceback.print_exc()
                # Don't fail the session creation, just log the error
        
        session = Session(
            session_id=session_id,
            name=session_data.name,
            description=session_data.description,
            created_at=timestamp,
            updated_at=timestamp,
            conversations_dir=conversations_dir_rel,
            conversations=[]
        )
        
        # Load existing sessions and add new one
        sessions_data = self._load_sessions_data()
        sessions_data.sessions.append(session)
        self._save_sessions_data(sessions_data)
        
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get a session by ID."""
        sessions_data = self._load_sessions_data()
        for session in sessions_data.sessions:
            if session.session_id == session_id:
                return session
        return None
    
    def list_sessions(self) -> List[Session]:
        """List all sessions."""
        sessions_data = self._load_sessions_data()
        return sessions_data.sessions
    
    def update_session(self, session_id: str, update_data: SessionUpdate) -> Optional[Session]:
        """Update a session."""
        sessions_data = self._load_sessions_data()
        
        for i, session in enumerate(sessions_data.sessions):
            if session.session_id == session_id:
                # Update fields if provided
                if update_data.name is not None:
                    session.name = update_data.name
                if update_data.description is not None:
                    session.description = update_data.description
                
                session.updated_at = self._get_current_timestamp()
                
                sessions_data.sessions[i] = session
                self._save_sessions_data(sessions_data)
                
                return session
        
        return None
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session (hard delete - removes everything)."""
        sessions_data = self._load_sessions_data()
        
        session_found = False
        updated_sessions = []
        
        for session in sessions_data.sessions:
            if session.session_id == session_id:
                session_found = True
                # Delete the session directory and all its contents
                session_dir = (self.sessions_dir / session_id).resolve()
                if session_dir.exists() and session_dir.is_dir():
                    try:
                        shutil.rmtree(str(session_dir))
                    except Exception as e:
                        # Log error but continue with deletion from JSON
                        print(f"Error: Failed to delete session directory {session_dir}: {e}")
                        # Still remove from JSON even if file deletion fails
            else:
                updated_sessions.append(session)
        
        if session_found:
            sessions_data.sessions = updated_sessions
            self._save_sessions_data(sessions_data)
            return True
        
        return False
    
    def delete_all_sessions(self) -> int:
        """Delete all sessions (hard delete - removes everything)."""
        sessions_data = self._load_sessions_data()
        
        deleted_count = 0
        
        # Delete all session directories
        for session in sessions_data.sessions:
            session_dir = (self.sessions_dir / session.session_id).resolve()
            if session_dir.exists() and session_dir.is_dir():
                try:
                    shutil.rmtree(str(session_dir))
                    deleted_count += 1
                except Exception as e:
                    print(f"Error: Failed to delete session directory {session_dir}: {e}")
        
        # Clear all sessions from JSON
        sessions_data.sessions = []
        self._save_sessions_data(sessions_data)
        
        return deleted_count
    
    def add_conversation(self, session_id: str, conversation_text: str) -> Optional[Conversation]:
        """Add a conversation to a session."""
        sessions_data = self._load_sessions_data()
        
        for i, session in enumerate(sessions_data.sessions):
            if session.session_id == session_id:
                # Generate conversation ID
                conversation_id = self._generate_conversation_id()
                timestamp = self._get_current_timestamp()
                
                # Store relative path
                conversation_file_rel = f"{session.conversations_dir}/{conversation_id}.txt"
                
                # Use absolute path for file operations
                conversation_file_abs = self.base_path / conversation_file_rel
                conversation_file_abs.parent.mkdir(parents=True, exist_ok=True)
                with open(conversation_file_abs, 'w', encoding='utf-8') as f:
                    f.write(conversation_text)
                
                conversation = Conversation(
                    conversation_id=conversation_id,
                    file_path=conversation_file_rel,
                    added_at=timestamp
                )
                
                # Save conversation to RAG service if available
                if self.rag_service:
                    try:
                        import asyncio
                        from ..rag import schemas as rag_schemas
                        # Create RAG conversation with the same session_id (UUID)
                        rag_conv_data = rag_schemas.ConversationCreate(
                            conv_text=conversation_text,
                            session_id=session_id  # Use the same UUID
                        )
                        # Run async function
                        asyncio.run(self.rag_service.save_conversation(rag_conv_data))
                        print(f"Successfully saved conversation to RAG for session: {session_id}")
                    except Exception as e:
                        print(f"Warning: Failed to save conversation to RAG: {e}")
                        import traceback
                        traceback.print_exc()
                        # Don't fail the conversation creation, just log the error
                
                # Update session
                session.conversations.append(conversation)
                session.last_conversation_added = timestamp
                session.updated_at = timestamp
                
                sessions_data.sessions[i] = session
                self._save_sessions_data(sessions_data)
                
                return conversation
        
        return None
    
    def get_conversation(self, session_id: str, conversation_id: str) -> Optional[Conversation]:
        """Get a specific conversation from a session."""
        session = self.get_session(session_id)
        if session:
            for conversation in session.conversations:
                if conversation.conversation_id == conversation_id:
                    return conversation
        return None
    
    def get_conversation_content(self, session_id: str, conversation_id: str) -> Optional[str]:
        """Get the content of a conversation file."""
        conversation = self.get_conversation(session_id, conversation_id)
        if not conversation:
            return None
        
        # Resolve the file path
        conversation_file = self.base_path / conversation.file_path
        if conversation_file.exists():
            try:
                with open(conversation_file, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"Error reading conversation file: {e}")
                return None
        return None
    
    def delete_conversation(self, session_id: str, conversation_id: str) -> bool:
        """Delete a conversation from a session (hard delete)."""
        sessions_data = self._load_sessions_data()
        
        for i, session in enumerate(sessions_data.sessions):
            if session.session_id == session_id:
                conversation_found = False
                updated_conversations = []
                
                for conversation in session.conversations:
                    if conversation.conversation_id == conversation_id:
                        conversation_found = True
                        # Delete the conversation file
                        conversation_file = (self.base_path / conversation.file_path).resolve()
                        if conversation_file.exists():
                            try:
                                conversation_file.unlink()
                            except Exception as e:
                                print(f"Error deleting conversation file {conversation_file}: {e}")
                    else:
                        updated_conversations.append(conversation)
                
                if conversation_found:
                    session.conversations = updated_conversations
                    session.updated_at = self._get_current_timestamp()
                    # Update last_conversation_added if needed
                    if not session.conversations:
                        session.last_conversation_added = None
                    else:
                        # Set to the most recent conversation
                        latest = max(session.conversations, key=lambda c: c.added_at)
                        session.last_conversation_added = latest.added_at
                    
                    sessions_data.sessions[i] = session
                    self._save_sessions_data(sessions_data)
                    return True
        
        return False
