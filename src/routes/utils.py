import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from starlette.status import *
from fastapi.responses import *
from datetime import datetime, timedelta


from ..services.session import Sessions, Session
from ..constants.config import SECRET_KEY, SESSION_TIMEOUT, REFRESH_SESSION_TIMEOUT
from ..models.user import Users
from .api_models import *


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

algorithm = "HS256"


def get_access_token(session_id: str, user_id: str) -> str:
    now = datetime.utcnow()
    payload = dict(
        session_id=session_id,
        user_id=user_id,
        iat=now,
        exp=now + timedelta(seconds=SESSION_TIMEOUT),
    )
    return jwt.encode(payload, SECRET_KEY, algorithm=algorithm)


def get_refresh_token(session_id: str, user_id: str) -> str:
    now = datetime.utcnow()
    payload = dict(
        session_id=session_id,
        user_id=user_id,
        iat=now,
        exp=now + timedelta(days=REFRESH_SESSION_TIMEOUT),
    )
    token = jwt.encode(payload, SECRET_KEY, algorithm=algorithm)
    return token


def token_from_payload(token: str = Depends(oauth2_scheme)) -> Session:
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[algorithm])

        if (session_id := payload.get("session_id")) and (
            session := Sessions.get(session_id)
        ):
            session: Session
            session.modified()
            return session
        elif user_id := payload.get("user_id"):
            if user := Users.find_child(user_id):
                return Sessions.create_session(user)
            else:
                raise HTTPException(
                    status_code=HTTP_405_METHOD_NOT_ALLOWED,
                    detail="Invalid Access Token: User does not exists.",
                )
        else:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Invalid Access Token: Session not found.",
            )
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=f"Expired Access Token: {e}",
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Access Token: {e}",
        )


def artisan_token_from_payload(token: str = Depends(oauth2_scheme)) -> Session:
    session = token_from_payload(token)
    if not session.client.user.is_artisan:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid Access Token: User is not an artisan",
        )
    else:
        return session


def client_token_from_payload(token: str = Depends(oauth2_scheme)) -> Session:
    session = token_from_payload(token)
    if not session.client.user.is_artisan:
        return session
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Expired Access Token: User is not an client",
        )


get_user_session: Session = Security(token_from_payload)
get_artisan_session: Session = Security(artisan_token_from_payload)
get_client_session: Session = Security(client_token_from_payload)
