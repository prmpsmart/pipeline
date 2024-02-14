from fastapi.middleware.cors import CORSMiddleware

from ..constants.config import *
from ..routes import routers
from .sio_server import *
from .utils import *


server = FastAPI(
    title=f"{FROM_NAME} REST API Server",
    lifespan=lifespan,
)

sio_server.other_asgi_app = server

server.mount("/ws", sio_app)

server.add_middleware(
    CORSMiddleware,
    allow_origins=wildcard,
    allow_methods=wildcard,
    allow_headers=wildcard,
    allow_credentials=True,
    expose_headers=wildcard,
)

server.include_router(routers)
