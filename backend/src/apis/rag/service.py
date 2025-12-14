import google.generativeai as genai
import chromadb
from chromadb.utils import embedding_functions
from sqlalchemy.future import select
from rank_bm25 import BM25Okapi
import numpy as np
from typing import Optional

from ...commons.database import AsyncSessionLocal
from ...commons.constants import settings
from . import models, schemas

class RagService:
    def __init__(self):
        # 1. Initialize Gemini
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.llm_model = genai.GenerativeModel(settings.GEMINI_MODEL)
        
        # 2. Initialize Vector DB (Chroma)
        self.chroma_client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
        self.embedding_fn = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
            api_key=settings.GOOGLE_API_KEY,
            model_name=settings.EMBEDDING_MODEL
        )
        self.collection = self.chroma_client.get_or_create_collection(
            name="conversations",
            embedding_function=self.embedding_fn
        )

    # --- Persistence Methods ---

    async def create_session(self, data: schemas.SessionCreate, session_id: Optional[str] = None) -> models.Session:
        # Use session_id from data if provided, otherwise use the parameter (for backward compatibility)
        final_session_id = data.session_id if data.session_id else session_id
        if not final_session_id:
            import uuid
            final_session_id = str(uuid.uuid4())
        
        async with AsyncSessionLocal() as db:
            session = models.Session(
                id=final_session_id,  # Use UUID as primary key
                name=data.session_name, 
                description=data.session_description
            )
            db.add(session)
            await db.commit()
            await db.refresh(session)
            return session

    async def get_all_sessions(self) -> list[models.Session]:
        """Get all sessions from RAG database."""
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(models.Session))
            sessions = result.scalars().all()
            return list(sessions)

    async def delete_all_sessions(self) -> int:
        """Delete all sessions from RAG database (hard delete)."""
        async with AsyncSessionLocal() as db:
            # Get all sessions first to count
            result = await db.execute(select(models.Session))
            sessions = result.scalars().all()
            count = len(sessions)
            
            # Delete all sessions (cascades to conversations)
            for session in sessions:
                await db.delete(session)
            
            await db.commit()
            
            # Also clear the vector database collection
            try:
                # Delete all documents from ChromaDB collection
                # Note: ChromaDB doesn't have a direct "delete all" method
                # We need to get all IDs and delete them
                all_docs = self.collection.get()
                if all_docs and all_docs.get('ids'):
                    self.collection.delete(ids=all_docs['ids'])
            except Exception as e:
                print(f"Warning: Failed to clear vector database: {e}")
            
            return count

    async def save_conversation(self, data: schemas.ConversationCreate) -> models.Conversation:
        async with AsyncSessionLocal() as db:
            # 1. Save to SQLite
            conv = models.Conversation(text=data.conv_text, session_id=data.session_id)
            db.add(conv)
            await db.commit()
            await db.refresh(conv)

            # 2. Index in Vector DB
            self.collection.add(
                ids=[str(conv.id)],
                documents=[conv.text],
                metadatas=[{"session_id": str(conv.session_id)}]  # UUID as string
            )
            return conv

    # --- Retrieval & RAG Methods ---

    def _hybrid_search(self, query: str, session_id: str) -> list[str]:
        # 1. Vector Search
        results = self.collection.query(
            query_texts=[query],
            n_results=settings.RAG_TOP_K * 2, # Fetch extra for re-ranking
            where={"session_id": str(session_id)}  # UUID as string
        )
        
        if not results['documents'] or not results['documents'][0]:
            return []

        docs = results['documents'][0]
        distances = results['distances'][0]
        
        # Normalize Vector Scores (1 - distance approximation)
        vec_scores = np.array([1 - d for d in distances])
        if vec_scores.size > 0:
            vec_scores = (vec_scores - vec_scores.min()) / (vec_scores.max() - vec_scores.min() + 1e-9)

        # 2. BM25 (Lexical) Search on retrieved docs
        tokenized_docs = [doc.split() for doc in docs]
        bm25 = BM25Okapi(tokenized_docs)
        bm25_scores = np.array(bm25.get_scores(query.split()))
        
        if bm25_scores.size > 0:
            bm25_scores = (bm25_scores - bm25_scores.min()) / (bm25_scores.max() - bm25_scores.min() + 1e-9)

        # 3. Weighted Fusion
        final_scores = (settings.RAG_VECTOR_WEIGHT * vec_scores) + (settings.RAG_BM25_WEIGHT * bm25_scores)
        
        # Sort and return top K
        sorted_indices = np.argsort(final_scores)[::-1][:settings.RAG_TOP_K]
        return [docs[i] for i in sorted_indices]

    async def stream_rag_response(self, query: str, session_id: str):
        # 1. Get Context
        context_docs = self._hybrid_search(query, session_id)
        context_text = "\n\n".join(context_docs)

        # 2. Prompt
        prompt = f"""
        Context from previous conversations:
        {context_text}
        
        User Question: {query}
        Answer based on context:
        """
        
        # 3. Stream
        response = self.llm_model.generate_content(prompt, stream=True)
        for chunk in response:
            if chunk.text:
                yield chunk.text