from fastapi import APIRouter

from ...models import *
from .api_models import *


transactions_router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)
