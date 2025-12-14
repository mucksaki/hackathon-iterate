from fastapi.responses import StreamingResponse, Response
from fastapi import HTTPException
from ...commons.router import make_router
from .service import TextToSpeechService
from .models import TextToSpeechRequest, VoiceOptions


@make_router()
def controller(router, text_to_speech_service: TextToSpeechService) -> None:
    @router.post("/tts")
    def tts(input_text: str, output_file: str, voice: VoiceOptions):
        inputs = TextToSpeechRequest(input_text=input_text, output_file=output_file, voice=voice)
        res = text_to_speech_service.run(inputs=inputs)
        return res
    
    @router.post("/generate")
    async def generate_audio(text: str, voice: str = "Eva"):
        """Generate audio from text and return as WAV file."""
        try:
            audio_data = await text_to_speech_service.generate_audio(text, voice)
            return Response(
                content=audio_data,
                media_type="audio/wav",
                headers={
                    "Content-Disposition": "attachment; filename=speech.wav"
                }
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate audio: {str(e)}")
