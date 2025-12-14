import os
from dotenv import load_dotenv
import gradium


SAMPLE_RATE = 48000


class TextToSpeechService:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GRADIUM_API_KEY")
        self.client = gradium.client.GradiumClient(api_key=api_key)

    async def stream_tts(self, text: str, voice: str, model_name: str = "default", output_format: str = "pcm"):
        gradium_stream = await self.client.tts_stream(
            setup={
                "model_name": model_name,
                "voice_id": voice,
                "output_format": output_format,
            },
            text=text,
        )
        async for audio_chunk in gradium_stream.iter_bytes():
            if audio_chunk:
                yield audio_chunk
