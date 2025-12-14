from fastapi.responses import StreamingResponse
from ...commons.router import make_router
from .service import RagService
from . import schemas

@make_router()
def controller(router, rag_service: RagService) -> None:

    @router.post("/save_session", response_model=schemas.SessionResponse)
    async def create_session(payload: schemas.SessionCreate):
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