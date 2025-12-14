from stt import upload_wav_to_pyannote, parse_conv, get_text
from typing import List

class SttService:
    def stt(self, file_path: str, object_key: str) -> List[dict[str, str]]:
        # file_path = 'backend/src/audios/sample_13-11-14-45.wav'
        # object_key = 'first-meeting'
        print('upload start ...')
        object_key = upload_wav_to_pyannote(file_path=file_path, object_key=object_key)
        print('upload finished')
        print('output start...')
        output = get_text(object_key=object_key)
        print('output finished')
        # print(f'output: \n {output}')
        return output
