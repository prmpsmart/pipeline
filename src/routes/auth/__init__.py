from fastapi import APIRouter


from ...services.mail.otp import ResetOTP
from ...utils.validators import Validator
from .utils import *


auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication / KYC"],
)


@auth_router.post(
    "/register_artisan",
    name="Register new Artisan Account",
    responses={
        HTTP_200_OK: {
            "model": LoginResponse,
            "description": "Signed Up successfully.",
        },
        HTTP_400_BAD_REQUEST: {
            "model": Response,
            "description": "Request body contains invalid data.",
        },
        HTTP_409_CONFLICT: {
            "model": Response,
            "description": "User with email or phone number already exists.",
        },
    },
)
async def register_artisan(
    request: ArtisanRegisterRequest,
) -> LoginResponse:
    email = request.email
    phone_number = request.phone_number
    detail = (
        Validator.validate(request.full_name, "Full Name")
        or Validator.validate_email(email)
        or Validator.validate_phone_number(phone_number)
        or Validator.validate_password(request.password)
    )

    user: User

    if detail:
        raise HTTPException(
            HTTP_400_BAD_REQUEST,
            detail=detail,
        )
    elif not (
        user := Users.find_one(
            search_or=dict(
                email=email,
                phone_number=phone_number,
            ),
        )
    ):
        user = Users.create(
            is_artisan=True,
            **request.model_dump(),
        )
        session: Session = Sessions.create_session(user)
        # session.client.send_otp()

        return get_login_response(
            session=session,
            detail=f"Account created successful. OTP has been sent to `{email}`",
        )
    else:
        # Users.delete_child(user._id)
        # print("deleting and recreating")
        # return await register_artisan(request)

        raise HTTPException(
            HTTP_409_CONFLICT,
            detail="User with provided details already exists.",
        )


@auth_router.post(
    "/register_client",
    name="Register new Client Account",
    responses={
        HTTP_200_OK: {
            "model": LoginResponse,
            "description": "Signed Up successfully.",
        },
        HTTP_400_BAD_REQUEST: {
            "model": Response,
            "description": "Request body contains invalid data.",
        },
        HTTP_409_CONFLICT: {
            "model": Response,
            "description": "User with email or phone number already exists.",
        },
    },
)
async def register_client(request: ClientRegisterRequest) -> LoginResponse:
    email = request.email
    detail = (
        Validator.validate(request.full_name, "Full Name")
        or Validator.validate_email(email)
        or Validator.validate_password(request.password)
        or Validator.validate(request.address, "Address")
        or Validator.validate(request.nationality, "Nationality")
        or Validator.validate_among(request.gender, ["male", "female"], "Gender")
        or Validator.validate(request.id_verification_image, "ID Card Image")
        or Validator.validate(request.age, "Age")
        or Validator.validate(request.id_verification, "ID Verification")
    )

    user: User

    if detail:
        raise HTTPException(
            HTTP_400_BAD_REQUEST,
            detail=detail,
        )
    elif not (user := Users.find_one(dict(email=email))):
        user: User = Users.create(
            is_artisan=False,
            **request.model_dump(),
        )

        session: Session = Sessions.create_session(user)
        # session.client.send_otp()

        return get_login_response(
            session=session,
            detail=f"Account created successful. OTP has been sent to `{email}`",
        )
    else:
        # Users.delete_child(user._id)

        raise HTTPException(
            HTTP_409_CONFLICT,
            detail="User with provided details already exists.",
        )


@auth_router.post(
    "/login",
    name="User Login",
    responses={
        HTTP_200_OK: {
            "model": LoginResponse,
            "description": "Login successful.",
        },
        HTTP_400_BAD_REQUEST: {
            "model": Response,
            "description": "Request body contains invalid data.",
        },
        HTTP_406_NOT_ACCEPTABLE: {
            "model": Response,
            "description": "Invalid `username`, `email`, or `password`.",
        },
    },
)
def login(request: LoginRequest) -> LoginResponse:
    email = request.email

    detail = Validator.validate_email(email) or Validator.validate_password(
        request.password
    )

    if detail:
        raise HTTPException(
            HTTP_400_BAD_REQUEST,
            detail=detail,
        )

    elif session := Sessions.get_by_email(request.email):
        return get_login_response(password=request.password, session=session)

    elif user := Users.find_one(dict(email=email)):
        return get_login_response(
            user=user,
            password=request.password,
        )

    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail=f"User with `email` `{email}` does not exists.",
        )


@auth_router.post(
    "/forgot_password",
    name="Forgot Password",
    responses={
        HTTP_200_OK: {
            "model": ForgotPasswordResponse,
            "description": "Reset OTP has been sent to email.",
        },
        HTTP_400_BAD_REQUEST: {
            "model": Response,
            "description": "Request body contains invalid data.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "User with email does not exists.",
        },
        HTTP_425_TOO_EARLY: {
            "model": ForgotPasswordResponse,
            "description": "Reset OTP has already been sent to email.",
        },
    },
)
async def forgot_password(
    request: ForgotPasswordRequest,
) -> ForgotPasswordResponse:
    email = request.email
    detail = Validator.validate_email(request.email)
    reset_otp: ResetOTP

    if detail:
        raise HTTPException(
            HTTP_400_BAD_REQUEST,
            detail=detail,
        )

    elif reset_otp := Sessions.get_reset(email):
        return ForgotPasswordResponse(
            detail=f"Reset OTP has already been sent to `{email}`",
            timeout=reset_otp.timeout,
            timeout_formated=reset_otp.timeout_formated,
            otp=reset_otp.otp,
        )

    elif reset_otp := Sessions.set_reset_password(email):
        reset_otp.send_otp()
        return ForgotPasswordResponse(
            detail=f"Reset OTP has been sent to `{email}`",
            timeout=reset_otp.timeout,
            timeout_formated=reset_otp.timeout_formated,
            otp=reset_otp.otp,
        )

    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail=f"User with email `{email}` does not exists.",
        )


@auth_router.post(
    "/reset_password",
    name="Reset Password",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Password reset successfully.",
        },
        HTTP_400_BAD_REQUEST: {
            "model": Response,
            "description": "Request body contains invalid data.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "No pending password reset for User with email.",
        },
        HTTP_406_NOT_ACCEPTABLE: {
            "model": Response,
            "description": "Invalid Reset OTP.",
        },
    },
)
async def reset_password(request: ResetPasswordRequest) -> Response:
    email = request.email
    detail = (
        Validator.validate_email(request.email)
        or Validator.validate_password(request.password)
        or Validator.validate(request.otp, "OTP")
    )
    if detail:
        raise HTTPException(HTTP_400_BAD_REQUEST, detail=detail)

    elif email not in Sessions.reset_otps:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail=f"No pending password reset for User with email `{email}`.",
        )
    elif Sessions.reset_password(email, request.password, request.otp):
        return Response(detail="Password reset successfully.")
    else:
        raise HTTPException(
            HTTP_406_NOT_ACCEPTABLE,
            detail="Invalid Reset OTP.",
        )


@auth_router.patch(
    "/profile",
    name="Update profile",
    responses={
        HTTP_200_OK: {
            "model": ProfileResponse,
            "description": "Profile updated successfully.",
        },
        HTTP_400_BAD_REQUEST: {
            "model": Response,
            "description": "Request body contains invalid data.",
        },
    },
)
async def profile(
    request: ProfileUpdateRequest,
    session: Session = get_user_session,
) -> ProfileResponse:
    if request.profile_image:
        if not is_link(request.profile_image):
            session.user.profile_image = upload_media(
                f"profile-image-{session.user.id}",
                request.profile_image,
                is_profile_image=True,
            )
    if request.id_verification:
        session.user.id_verification = request.id_verification
    if request.id_verification_image:
        if not is_link(request.id_verification_image):
            session.user.id_verification_image = upload_media(
                f"id-card-image-{session.user.id}",
                request.id_verification_image,
                is_identity_image=True,
            )
    if request.location:
        session.user.location = request.location
    if request.pin:
        session.user.pin = request.pin
    if request.nationality:
        session.user.nationality = request.nationality
    if request.profession:
        session.user.profession = request.profession
    if request.about:
        session.user.about = request.about
    if request.education:
        session.user.education = request.education
    if request.security_question:
        session.user.security_question = request.security_question
    if request.security_answer:
        session.user.security_answer = request.security_answer

    session.user.save()

    return ProfileResponse(
        detail="Profile updated successfully",
        user=get_user_data(session.user),
        is_artisan=session.user.is_artisan,
    )
