from fastapi.responses import StreamingResponse
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
