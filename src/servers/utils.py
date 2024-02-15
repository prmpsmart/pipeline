from fastapi import FastAPI
from contextlib import asynccontextmanager

from ..services.mail.gmail import GmailSend


# from ..constants.config import LOGGER
# from ..models import *
from ..utils.commons import run_on_thread
from ..routes.utils import *
from .sio_server import *

# from ..mail.gmail import GmailSend


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_on_thread(Sessions.clear_sessions)
    # GmailSend.setup()

    yield

    GmailSend.kill()
    Sessions.kill()
    await sio_server.shutdown()


async def emit_to_user(user_id: str, event: str, data: dict):
    if user_session := Sessions.get_by_user_id(user_id):
        user_session: Session
        if user_session.client.sid:
            await sio_server.emit(
                event,
                data=data,
                to=user_session.client.sid,
                namespace=ns,
            )
