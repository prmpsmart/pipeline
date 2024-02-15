from urllib.parse import urlparse
from ...utils.commons import verify_hash
from .api_models import *
from ...models.user import *


def is_link(text: str):
    try:
        return bool(urlparse(text).scheme)
    except:
        return False


def get_user_data(user: User):
    return UserData(
        id=user.id,
        created_timestamp=user.created_timestamp,
        email=user.email,
        phone_number=user.phone_number,
        full_name=user.full_name,
        image=user.image,
    )


def get_login_response(
    user: User = None,
    session: Session = None,
    detail: str = "Login successful.",
    password: str = "",
) -> LoginResponse:
    user = user or session.user
    if password and not verify_hash(password, user.password):
        raise HTTPException(
            HTTP_406_NOT_ACCEPTABLE,
            detail="Invalid `email`, or `password`.",
        )

    session = (
        session or Sessions.get_by_email(user.email) or Sessions.create_session(user)
    )
    return LoginResponse(
        detail=detail,
        access_token=get_access_token(
            session.id,
            user.id,
        ),
        user=get_user_data(user),
    )
