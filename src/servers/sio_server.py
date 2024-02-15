from socketio import AsyncServer, ASGIApp

from ..constants.config import LOGGER
from ..routes.utils import *


wildcard = ["*"]

ns = ""

sio_server = AsyncServer(
    cors_allowed_origins=wildcard,
    async_mode="asgi",
    logger=True,
    # engineio_logger=True,
    namespaces=ns,
)

sio_app = ASGIApp(
    socketio_server=sio_server,
    socketio_path="ws",
)


@sio_server.on("connect", namespace=ns)
async def connect(sid: str, environ: dict, auth: dict):
    token = auth.get("token", "")

    LOGGER.info(f"connect - `{sid}`, token - `{token}`")
    if token:
        try:
            session: Session = token_from_payload(token)
            Sessions.set_session_sid(sid, session)
            await sio_server.emit("connected")

        except HTTPException as e:
            await sio_server.emit("error", dict(detail=e.detail))
            await sio_server.disconnect(sid)
    else:
        await sio_server.emit("error", dict(detail="Provide a token"))
        await sio_server.disconnect(sid)


@sio_server.on("disconnect", namespace=ns)
async def disconnect(sid: str):
    if session := Sessions.remove_session_sid(sid):
        await sio_server.emit(
            "status",
            data=dict(
                user_id=session.user.id,
                sid=sid,
                online=False,
            ),
            skip_sid=sid,
        )


@sio_server.on("newMessage", namespace=ns)
async def newMessage(sid: str, data: dict):
    LOGGER.info("new message received")
    if session := Sessions.sids.get(sid):
        LOGGER.info("new message received 2")
        message: Message = Messages.create(**data)
        print(message.dict)

        await sio_server.emit(
            "newMessage",
            data=message.dict,
            to=sid,
            namespace=ns,
        )
        other_session: Session = None
        if session.user.is_elder:
            other_session = Sessions.get_by_user_id(message.caregiver)
        else:
            other_session = Sessions.get_by_user_id(message.elder)

        if other_session and other_session.client.sid:
            await sio_server.emit(
                "newMessage",
                data=message.dict,
                to=other_session.client.sid,
                namespace=ns,
            )


@sio_server.on("allMessages", namespace=ns)
async def allMessages(sid: str, other_user_id: str):
    LOGGER.info(f"all messages received - {other_user_id}")
    if session := Sessions.sids.get(sid):
        LOGGER.info("all messages received 2")
        filters = {}
        session: Session
        if session.user.is_elder:
            filters.update(
                elder=session.user.id,
                caregiver=other_user_id,
            )
        else:
            filters.update(
                caregiver=session.user.id,
                elder=other_user_id,
            )

        messages = Messages.find(filters)
        msgs = [msg.dict for msg in messages]
        print(msgs)

        await sio_server.emit(
            "allMessages",
            data=dict(messages=msgs),
            to=sid,
            namespace=ns,
        )
