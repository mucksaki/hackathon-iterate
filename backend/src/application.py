from .commons.router import MyFastAPI
from .apis.example.controller import controller as example_controller
from .apis.example.service import ExampleService
from .apis.session_manager.controller import controller as session_manager_controller
from .apis.session_manager.service import SessionService

from .apis.speech_to_text.service import SttService
from .apis.speech_to_text.controller import controller as SttControler

import asyncio
from contextlib import asynccontextmanager

from .commons.router import MyFastAPI
from .commons.database import engine
from .apis.rag import models as rag_models

# Import Controllers
from .apis.rag.controller import controller as rag_controller

# Import Services
from .apis.rag.service import RagService

@asynccontextmanager
async def lifespan(app: MyFastAPI):
    # Ensure DB tables exist on startup
    async with engine.begin() as conn:
        await conn.run_sync(rag_models.Base.metadata.create_all)
    print("Database tables created.")
    yield
    print("Shutting down...")

app = MyFastAPI(root="/api", lifespan=lifespan)
rag_service = RagService()
# Configure services
example_service = ExampleService()
session_service = SessionService()
stt_service = SttService()

# Configure controllers
controller_configs = [
    ("/example", example_controller, {"example_service": example_service}),
    ("/session-manager", session_manager_controller, {"session_service": session_service}),
    ("/speech_to_text", SttControler, {'stt_service': stt_service}),
    ("/rag", rag_controller, {"rag_service": rag_service}),
]

for path, controller, kwargs in controller_configs:
    app.add_controller(path, controller, **kwargs)

print("Application startup completed.")
