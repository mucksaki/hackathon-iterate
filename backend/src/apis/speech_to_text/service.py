from .stt import upload_wav_to_pyannote, parse_conv, get_text
from typing import List
from .models import SpeechToTextInput

class SttService:
    def stt(self, stt_input: SpeechToTextInput) -> List[dict[str, str]]:
        print('upload start ...')
        upload_wav_to_pyannote(file_path=stt_input.file_path, object_key=stt_input.object_key)
        print('upload finished')
        print('output start...')
        output = get_text(object_key=stt_input.object_key)
        print('output finished')
        return output
