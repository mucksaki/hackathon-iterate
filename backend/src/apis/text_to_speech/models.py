from pydantic import BaseModel


class TextToSpeechRequest(BaseModel):
    text: str
    voice: str
    model_name: str = "default"
    output_format: str = "pcm"