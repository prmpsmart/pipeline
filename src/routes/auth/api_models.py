from typing import Optional
from ..utils import *
from ..api_models import *


class ClientData(BaseModel):
    id: str
    created_timestamp: int

    email: str
    phone_number: str
    full_name: str
    address: str
    password: str

    last_seen: int
    profile_image: str
    gender: str
    age: int
    id_verification: str
    id_verification_image: str
    location: str
    pin: str
    nationality: str

    verifiedEmail: bool
    verifiedID: bool
    verifiedPhoneNumber: bool


class ArtisanData(ClientData):
    profession: str
    about: str
    education: str
    security_question: str
    security_answer: str
    job_delivery_time: int
    last_job_delivery: int


class ProfileUpdateRequest(BaseModel):
    # gender: Optional[str]
    # age: Optional[int]
    profile_image: Optional[str]
    id_verification: Optional[str]
    id_verification_image: Optional[str]
    location: Optional[str]
    pin: Optional[str]
    nationality: Optional[str]
    profession: Optional[str]
    about: Optional[str]
    education: Optional[str]
    security_question: Optional[str]
    security_answer: Optional[str]


class ArtisanRegisterRequest(BaseModel):
    full_name: str
    email: str
    phone_number: str
    password: str

    # profession: str
    # about: str
    # education: str
    # profile_image: str
    # age: int
    # id_verification: str
    # id_verification_image: str


class ClientRegisterRequest(BaseModel):
    full_name: str
    email: str
    password: str
    address: str

    # nationality: str
    # gender: str
    # id_verification_image: str
    # age: int
    # id_verification: str


class LoginRequest(BaseModel):
    email: str
    password: str


class ProfileResponse(Response):
    user: ClientData | ArtisanData
    is_artisan: bool


class LoginResponse(SessionResponse, ProfileResponse): ...


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
