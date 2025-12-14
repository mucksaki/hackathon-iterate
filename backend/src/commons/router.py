from functools import wraps
from fastapi import APIRouter, FastAPI


class MyFastAPI(FastAPI):
    def add_controller(self, prefix_path: str, controller: callable, *args, **kwargs):
        if prefix_path.endswith("/"):
            prefix_path = prefix_path[:-1]
        self.include_router(controller(prefix_path, *args, **kwargs))


def make_router(name: str = None, **rkwargs):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            rkwargs["prefix"] = args[0]
            if name is not None:
                rkwargs["tags"] = [name]
            if "tags" not in rkwargs:
                rkwargs["tags"] = [args[0]]
            router = APIRouter(**rkwargs)
            new_args = [router] + list(args[1:])
            function(*new_args, **kwargs)
            return router

        return wrapper

    return decorator
