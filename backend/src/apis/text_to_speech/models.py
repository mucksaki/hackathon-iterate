from pydantic import BaseModel
from enum import Enum

class TextToSpeechRequest(BaseModel):
    input_text: str
    output_file: str
    voice: str
    
class VoiceOptions(str, Enum):
    """Voice options for Text-to-Speech."""
    EVA = "Eva"
    EMMA = "Emma"
    JACK = "Jack"