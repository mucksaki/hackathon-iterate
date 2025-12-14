from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Session(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True, index=True)  # UUID from session_manager
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    conversations = relationship("Conversation", back_populates="session")

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    session_id = Column(String, ForeignKey("sessions.id"))  # UUID reference
    created_at = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("Session", back_populates="conversations")