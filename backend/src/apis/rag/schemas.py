from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Request Models
class SessionCreate(BaseModel):
    session_name: str
    session_description: Optional[str] = None
    session_id: Optional[str] = None  # UUID - if not provided, will be generated

class ConversationCreate(BaseModel):
    conv_text: str
    session_id: str  # UUID

class QueryRequest(BaseModel):
    query: str
    session_id: str  # UUID

# Response Models
class SessionResponse(BaseModel):
    id: str  # UUID
    name: str
    description: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: int
    text: str
    session_id: str  # UUID
    created_at: datetime
    class Config:
        from_attributes = True