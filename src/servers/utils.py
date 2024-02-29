from fastapi import FastAPI
from contextlib import asynccontextmanager

from ..services.mail.gmail import GmailSend


# from ..constants.config import LOGGER
# from ..models import *
from ..utils.commons import run_on_thread
from ..routes.utils import *

# from ..mail.gmail import GmailSend


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_on_thread(Sessions.clear_sessions)
    # GmailSend.setup()

    yield

    GmailSend.kill()
    Sessions.kill()
