from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Request Models
class SessionCreate(BaseModel):
    session_name: str
    session_description: Optional[str] = None

class ConversationCreate(BaseModel):
    conv_text: str
    session_id: int

class QueryRequest(BaseModel):
    query: str
    session_id: int

# Response Models
class SessionResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: int
    text: str
    session_id: int
    created_at: datetime
    class Config:
        from_attributes = True