import google.generativeai as genai
from app.config import settings

class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)

    async def stream_rag_response(self, query: str, context_docs: list[str]):
        """
        Constructs the prompt and streams the response from Gemini.
        """
        # Construct Context Block
        context_text = "\n\n".join(context_docs)
        
        prompt = f"""
        You are a helpful AI assistant named Clara. Use the following context from previous conversations to answer the user's question.
        
        Context:
        {context_text}
        
        User Question: {query}
        
        Answer:
        """
        
        # Streaming call
        response = self.model.generate_content(prompt, stream=True)
        
        for chunk in response:
            if chunk.text:
                yield chunk.text

llm_service = GeminiService()