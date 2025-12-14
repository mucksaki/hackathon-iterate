from pydantic import BaseModel

class SpeechToTextInput(BaseModel):
    file_path: str
    object_key: str