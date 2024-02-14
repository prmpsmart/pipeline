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
    return (
        ArtisanData(
            id=user.id,
            created_timestamp=user.created_timestamp,
            email=user.email,
            phone_number=user.phone_number,
            full_name=user.full_name,
            password=user.password,
            last_seen=user.last_seen,
            profile_image=user.profile_image,
            gender=user.gender,
            age=user.age,
            id_verification=user.id_verification,
            id_verification_image=user.id_verification_image,
            location=user.location,
            pin=user.pin,
            address=user.address,
            nationality=user.nationality,
            verifiedEmail=user.verifiedEmail,
            verifiedID=user.verifiedID,
            verifiedPhoneNumber=user.verifiedPhoneNumber,
            #
            profession=user.profession,
            about=user.about,
            education=user.education,
            security_question=user.security_question,
            security_answer=user.security_answer,
            job_delivery_time=user.job_delivery_time,
            last_job_delivery=user.last_job_delivery,
        )
        if user.is_artisan
        else ClientData(
            id=user.id,
            created_timestamp=user.created_timestamp,
            email=user.email,
            phone_number=user.phone_number,
            full_name=user.full_name,
            password=user.password,
            last_seen=user.last_seen,
            profile_image=user.profile_image,
            gender=user.gender,
            age=user.age,
            id_verification=user.id_verification,
            id_verification_image=user.id_verification_image,
            location=user.location,
            pin=user.pin,
            address=user.address,
            nationality=user.nationality,
            verifiedEmail=user.verifiedEmail,
            verifiedID=user.verifiedID,
            verifiedPhoneNumber=user.verifiedPhoneNumber,
        )
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
            detail="Invalid `username`, `email`, or `password`.",
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
        is_artisan=user.is_artisan,
    )
