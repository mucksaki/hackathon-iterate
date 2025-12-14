import os
from dotenv import load_dotenv
import gradium
from fastapi import HTTPException
from .text_to_speech import test_tts_stream, test_tts
from .models import TextToSpeechRequest
import asyncio
import json
from typing import Optional


SAMPLE_RATE = 48000
# voices_file_path = "backend/src/apis/text_to_speech/voices.json"
# test = json.load(open(voices_file_path))

voice_id_dict ={"Eva": "ubuXFxVQwVYnZQhy", "Jack":"m86j6D7UZpGzHsNu", "Emma": "YTpq7expH9539ERJ"}

class TextToSpeechService:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GRADIUM_API_KEY")
        if not api_key:
            raise RuntimeError("GRADIUM_API_KEY is not set in environment")
        self.client = gradium.client.GradiumClient(api_key=api_key)
    
    def run(self, inputs: TextToSpeechRequest):
        voice_id = voice_id_dict[inputs.voice]
        print(voice_id)
        output_path = f"{inputs.output_file}.wav"
        print(output_path)
        asyncio.run(test_tts(client=self.client, text=inputs.input_text, voice=voice_id, output_file=output_path))
        return {"message": "TTS request completed."}
    
    async def generate_audio(self, text: str, voice: str = "Eva") -> bytes:
        """Generate audio from text and return as bytes."""
        voice_id = voice_id_dict.get(voice, voice_id_dict["Eva"])
        result = await self.client.tts(
            setup={
                "model_name": "default", 
                "voice_id": voice_id,
                "output_format": "wav"
            },
            text=text
        )
        return result.raw_data
   