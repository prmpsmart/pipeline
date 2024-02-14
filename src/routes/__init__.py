from fastapi import APIRouter
from .auth import auth_router


routers = APIRouter()
routers.include_router(auth_router)
