from typing import Optional
from ..utils import *
from ..api_models import *


class UserData(BaseModel):
    id: str
    created_timestamp: int

    full_name: str
    email: str

    phone_number: str
    image: str


class RegisterRequest(BaseModel):
    full_name: str
    email: str

    phone_number: str
    password: str
    image: Optional[str]


class ProfileUpdateRequest(BaseModel):
    full_name: Optional[str]
    email: Optional[str]

    phone_number: Optional[str]
    image: Optional[str]


class LoginRequest(BaseModel):
    email: str
    password: str


class ProfileResponse(Response):
    user: UserData


class LoginResponse(SessionResponse, ProfileResponse):
    ...


class ForgotPasswordRequest(BaseModel):
    email: str


class ForgotPasswordResponse(Response):
    timeout: int
    otp: int
    timeout_formated: str


class ResetPasswordRequest(BaseModel):
    email: str
    otp: int
    password: str
