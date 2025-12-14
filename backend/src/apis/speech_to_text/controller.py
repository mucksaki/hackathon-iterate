from .service import SttService
from ...commons.router import make_router


@make_router()
def controller(router, example_service: SttService) -> None:
    @router.get("/tts")
    def stt():
        res = example_service.stt()
        return res
