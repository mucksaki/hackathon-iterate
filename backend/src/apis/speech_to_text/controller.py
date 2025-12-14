from .service import SttService
from ...commons.router import make_router
from .models import SpeechToTextInput


@make_router()
def controller(router, stt_service: SttService) -> None:
    @router.post("/stt")
    def stt(file_path: str, object_key: str):
        stt_input = SpeechToTextInput(file_path=file_path, object_key=object_key)
        res = stt_service.stt(stt_input)
        return res
