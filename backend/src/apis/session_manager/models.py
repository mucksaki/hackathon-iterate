from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class Conversation(BaseModel):
    conversation_id: str
    file_path: str
    added_at: str
    chunk_count: Optional[int] = 0
    status: Optional[str] = "pending"  # pending, chunked, error


class Session(BaseModel):
    session_id: str
    name: str
    description: Optional[str] = None
    created_at: str
    updated_at: str
    conversations_dir: str
    last_conversation_added: Optional[str] = None
    conversations: List[Conversation] = []


class SessionCreate(BaseModel):
    name: str
    description: Optional[str] = None


class SessionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ConversationCreate(BaseModel):
    text: str


class SessionsData(BaseModel):
    sessions: List[Session] = []

