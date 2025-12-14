from .commons.router import MyFastAPI
from .apis.example.controller import controller as example_controller
from .apis.example.service import ExampleService
from .apis.session_manager.controller import controller as session_manager_controller
from .apis.session_manager.service import SessionService

app = MyFastAPI(root="/api")

# Configure services
example_service = ExampleService()
session_service = SessionService()

# Configure controllers
controller_configs = [
    ("/example", example_controller, {"example_service": example_service}),
    ("/session-manager", session_manager_controller, {"session_service": session_service}),
]

for path, controller, kwargs in controller_configs:
    app.add_controller(path, controller, **kwargs)

print("Application startup completed.")
