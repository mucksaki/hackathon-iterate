from fastapi.responses import StreamingResponse
from ...commons.router import make_router
from .service import RagService
from . import schemas

@make_router()
def controller(router, rag_service: RagService) -> None:

    @router.post("/save_session", response_model=schemas.SessionResponse)
    async def create_session(payload: schemas.SessionCreate):
        # session_id can be provided in payload, or will be generated in service
        return await rag_service.create_session(payload)

    @router.post("/save_conversation", response_model=schemas.ConversationResponse)
    async def save_conversation(payload: schemas.ConversationCreate):
        return await rag_service.save_conversation(payload)

    @router.post("/initial_query")
    async def initial_query(payload: schemas.QueryRequest):
        # Get generator from service
        response_generator = rag_service.stream_rag_response(payload.query, payload.session_id)
        # Return standard StreamingResponse
        return StreamingResponse(response_generator, media_type="text/event-stream")

    @router.get("/sessions", response_model=list[schemas.SessionResponse])
    async def get_all_sessions():
        """Get all sessions from RAG database."""
        return await rag_service.get_all_sessions()

    @router.delete("/sessions", status_code=200)
    async def delete_all_sessions():
        """Delete all sessions from RAG database (hard delete)."""
        deleted_count = await rag_service.delete_all_sessions()
        return {"message": f"Deleted {deleted_count} session(s) from RAG"}