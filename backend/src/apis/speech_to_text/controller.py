from .service import ExampleService
from ...commons.router import make_router


@make_router()
def controller(router, example_service: ExampleService) -> None:
    @router.get("/good_boy")
    def good_boy():
        res = example_service.good_boy()
        return res
