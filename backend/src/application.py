from .commons.router import MyFastAPI
from .apis.example.controller import controller as example_controller
from .apis.example.service import ExampleService

app = MyFastAPI(root="/api")

# Configure services
example_service = ExampleService()

# Configure controllers
controller_configs = [
    ("/example", example_controller, {"example_service": example_service}),
]

for path, controller, kwargs in controller_configs:
    app.add_controller(path, controller, **kwargs)

print("Application startup completed.")
