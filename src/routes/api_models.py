from pydantic import BaseModel


class Response(BaseModel):
    detail: str


class SessionResponse(Response):
    access_token: str
