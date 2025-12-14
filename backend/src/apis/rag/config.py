import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "Gemini Hybrid RAG"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./sql_app.db"
    
    # Vector Store & RAG
    VECTOR_DB_PATH: str = "./chroma_db"
    EMBEDDING_MODEL: str = "models/embedding-001" # Gemini Embedding
    RAG_TOP_K: int = 5
    RAG_VECTOR_WEIGHT: float = 0.7
    RAG_BM25_WEIGHT: float = 0.3
    
    # LLM
    GOOGLE_API_KEY: str = "projects/659427817649"
    GEMINI_MODEL: str = "gemini-1.5-flash"

    class Config:
        env_file = ".env"

settings = Settings()