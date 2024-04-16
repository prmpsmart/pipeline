from fastapi import APIRouter

from ...models import *
from ...services.mail.otp import ResetOTP
from ...services.mail.gmail import GmailSend
from ...utils.validators import Validator
from .utils import *


auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication / KYC"],
)


@auth_router.post(
    "/register",
    name="Register new user",
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
async def register(
    request: RegisterRequest,
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
    detail = ""

    if detail:
        raise HTTPException(
            HTTP_400_BAD_REQUEST,
            detail=detail,
        )
    elif not (
        user := Users.find_one(
            search_or=[
                dict(
                    email=email,
                    phone_number=phone_number,
                )
            ],
        )
    ):
        user = Users.create(
            **request.model_dump(),
        )
        session: Session = Sessions.create_session(user)
        # session.client.send_otp()

        for name in ["Personal", "Business"]:
            MainPipelines.create(
                name=name,
                email=user.email,
                percentage=0,
            )

        return get_login_response(
            session=session,
            detail=f"Account created successfully. OTP has been sent to `{email}`",
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
    "/login",
    name="User Login",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Verify login in email.",
        },
        HTTP_400_BAD_REQUEST: {
            "model": Response,
            "description": "Request body contains invalid data.",
        },
        HTTP_406_NOT_ACCEPTABLE: {
            "model": Response,
            "description": "Invalid `email`, or `password`.",
        },
    },
)
def login(request: LoginRequest) -> Response:
    email = request.email
    password = request.password

    detail = Validator.validate_email(email) or Validator.validate_password(password)

    if detail:
        raise HTTPException(
            HTTP_400_BAD_REQUEST,
            detail=detail,
        )

    # elif session := Sessions.get_by_email(request.email):
    #     return get_login_response(
    #         password=request.password,
    #         session=session,
    #     )

    elif user := Users.find_one(dict(email=email)):
        user: User
        if verify_hash(password, user.password):
            now = datetime.now()
            payload = dict(
                user_id=user.id,
                iat=now,
                exp=now + timedelta(minutes=10),
            )
            token = jwt.encode(payload, SECRET_KEY, algorithm=algorithm)

            # send the email now
            link = f"http://pipeline-beta.vercel.app/verifyLogin?token={token}"

            GmailSend.send(
                user.email,
                user.full_name,
                "Verify Login",
                f"Click this link to verify your login {link}",
            )

            return Response(detail="Verify login in email")

        # return get_login_response(
        #     user=user,
        #     password=request.password,
        # )
        else:
            raise HTTPException(
                HTTP_406_NOT_ACCEPTABLE,
                detail=f"Invalid password.",
            )

    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail=f"User with `email` `{email}` does not exists.",
        )


@auth_router.get(
    "/verifyLogin",
    name="Verify User Login",
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
            "description": "Invalid `email`, or `password`.",
        },
    },
)
def verifyLogin(token: str) -> LoginResponse:
    try:
        payload = jwt.decode(token)
        if user := Users.find_child(payload["user_id"]):
            return get_login_response(user=user)

        else:
            raise HTTPException(
                HTTP_404_NOT_FOUND,
                detail=f"User with `email` `{email}` does not exists.",
            )
    except:
        raise HTTPException(HTTP_406_NOT_ACCEPTABLE, detail="Bad verification token")


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


@auth_router.get(
    "/profile",
    name="Get profile",
    responses={
        HTTP_200_OK: {
            "model": ProfileResponse,
            "description": "Profile returned successfully.",
        },
        HTTP_400_BAD_REQUEST: {
            "model": Response,
            "description": "Request body contains invalid data.",
        },
    },
)
async def profile(session: Session = get_user_session) -> ProfileResponse:
    return ProfileResponse(
        detail="Profile returned successfully",
        user=get_user_data(session.user),
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
    session.user.update(**request.model_dump())
    return ProfileResponse(
        detail="Profile updated successfully",
        user=get_user_data(session.user),
    )
