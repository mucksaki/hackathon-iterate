import chromadb
from chromadb.utils import embedding_functions
import google.generativeai as genai
from rank_bm25 import BM25Okapi
from typing import List, Dict, Any
import numpy as np

from app.config import settings

# Configure Gemini
genai.configure(api_key=settings.GOOGLE_API_KEY)

class HybridRetriever:
    def __init__(self):
        # Initialize ChromaDB (Persistent)
        self.chroma_client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
        
        # Use Google Generative AI Embedding Function
        self.embedding_fn = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
            api_key=settings.GOOGLE_API_KEY,
            model_name=settings.EMBEDDING_MODEL
        )
        
        self.collection = self.chroma_client.get_or_create_collection(
            name="conversations",
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"}
        )

    def add_document(self, doc_id: str, text: str, metadata: Dict[str, Any]):
        """
        Adds a document to the vector store.
        """
        self.collection.add(
            ids=[doc_id],
            documents=[text],
            metadatas=[metadata]
        )

    def _get_bm25_scores(self, query: str, documents: List[str]) -> np.ndarray:
        """
        Calculates BM25 scores for a list of documents against a query.
        """
        if not documents:
            return np.array([])
        
        tokenized_docs = [doc.split() for doc in documents]
        bm25 = BM25Okapi(tokenized_docs)
        tokenized_query = query.split()
        return np.array(bm25.get_scores(tokenized_query))

    def hybrid_search(self, query: str, session_id: int, top_k: int = settings.RAG_TOP_K) -> List[str]:
        """
        Performs hybrid retrieval:
        1. Fetch candidates from Vector DB (filtered by session_id).
        2. Perform BM25 on these candidates (or a larger pool).
        3. Combine scores.
        """
        
        # 1. Vector Search (Dense)
        # We fetch slightly more than top_k to allow re-ranking flexibility
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k * 2, 
            where={"session_id": session_id}
        )
        
        if not results['documents'] or not results['documents'][0]:
            return []

        docs = results['documents'][0]
        ids = results['ids'][0]
        distances = results['distances'][0] # Chroma returns distance (lower is better for cosine)

        # Convert cosine distance to similarity score (approx 1 - distance)
        # Note: Chroma distance behavior depends on space configuration. 
        # Assuming cosine distance where 0 is identical.
        vector_scores = np.array([1 - d for d in distances])
        
        # Normalize Vector Scores (0 to 1)
        if vector_scores.size > 0:
            v_min, v_max = vector_scores.min(), vector_scores.max()
            if v_max - v_min > 0:
                vector_scores = (vector_scores - v_min) / (v_max - v_min)
            else:
                vector_scores = np.ones_like(vector_scores)

        # 2. BM25 Search (Lexical) on the retrieved context
        # In a massive system, you'd use a dedicated search engine. 
        # For session-based RAG, re-ranking retrieved vector candidates is efficient.
        bm25_scores = self._get_bm25_scores(query, docs)
        
        # Normalize BM25 Scores
        if bm25_scores.size > 0:
            b_min, b_max = bm25_scores.min(), bm25_scores.max()
            if b_max - b_min > 0:
                bm25_scores = (bm25_scores - b_min) / (b_max - b_min)
            else:
                bm25_scores = np.zeros_like(bm25_scores)

        # 3. Weighted Fusion
        final_scores = (
            (settings.RAG_VECTOR_WEIGHT * vector_scores) + 
            (settings.RAG_BM25_WEIGHT * bm25_scores)
        )

        # Sort by final score
        sorted_indices = np.argsort(final_scores)[::-1][:top_k]
        
        return [docs[i] for i in sorted_indices]

# Singleton instance
rag_engine = HybridRetriever()