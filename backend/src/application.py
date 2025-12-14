from .commons.router import MyFastAPI
from .apis.example.controller import controller as example_controller
from .apis.example.service import ExampleService
from .apis.text_to_speech.controller import controller as text_to_speech_controller
from .apis.text_to_speech.service import TextToSpeechService

app = MyFastAPI(root="/api")

# Configure services
example_service = ExampleService()
text_to_speech_service = TextToSpeechService()

# Configure controllers
controller_configs = [
    ("/example", example_controller, {"example_service": example_service}),
    ("/text_to_speech", text_to_speech_controller, {"text_to_speech_service": text_to_speech_service})
]

for path, controller, kwargs in controller_configs:
    app.add_controller(path, controller, **kwargs)

print("Application startup completed.")
