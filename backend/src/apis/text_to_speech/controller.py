from fastapi.responses import StreamingResponse
from ...commons.router import make_router
from .service import TextToSpeechService
from .models import TextToSpeechRequest


@make_router()
def controller(router, text_to_speech_service: TextToSpeechService) -> None:
    @router.post("/tts")
    async def tts(req: TextToSpeechRequest):
        stream = text_to_speech_service.stream_tts(
            text=req.text,
            voice=req.voice,
            model_name=req.model_name,
            output_format=req.output_format,
        )
        return StreamingResponse(stream, media_type="audio/L16; rate=48000")
