from pydantic_settings import BaseSettings
from pathlib import Path
from pydantic import field_validator
import os


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./sql_app.db"
    
    # RAG & LLM
    GOOGLE_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.0-flash"
    EMBEDDING_MODEL: str = "models/embedding-001"
    VECTOR_DB_PATH: str = "./chroma_db"
    
    # Tuning
    RAG_TOP_K: int = 5
    RAG_VECTOR_WEIGHT: float = 0.7
    RAG_BM25_WEIGHT: float = 0.3
    
    @field_validator('GOOGLE_API_KEY')
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("GOOGLE_API_KEY is required and cannot be empty")
        return v.strip()

    class Config:
        # Load .env from root folder (two levels up from this file)
        # Calculate path relative to this file's location
        _env_file_path = Path(__file__).parent.parent.parent.parent / ".env"
        env_file = str(_env_file_path.resolve())
        extra = "ignore"  # Ignore extra fields from .env that aren't in the model

settings = Settings()

# Debug: Check if API key is loaded (remove in production)
if not settings.GOOGLE_API_KEY:
    env_file_path = Path(__file__).parent.parent.parent.parent / ".env"
    print(f"WARNING: GOOGLE_API_KEY is empty or not set!")
    print(f"Looking for .env at: {env_file_path.resolve()}")
    print(f".env file exists: {env_file_path.exists()}")
    if env_file_path.exists():
        print(f"Contents of .env (first 200 chars): {env_file_path.read_text()[:200]}")