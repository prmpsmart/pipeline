from fastapi import APIRouter
from .auth import auth_router
from .pipelines import pipelines_router
from .transactions import transactions_router


routers = APIRouter()
routers.include_router(auth_router)
routers.include_router(pipelines_router)
# routers.include_router(transactions_router)
