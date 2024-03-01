from typing import Optional
from ..utils import *
from ..api_models import *


class TransactionType(Enum):
    received = "received"
    sent = "sent"


class TransactionModel(BaseModel):
    id: str
    created_timestamp: int

    type: TransactionType
    amount: float
    status: str

    from_main_pipeline: str
    from_branch_pipeline: str

    to_main_pipeline: str
    to_branch_pipeline: str

    sender: str
    sender_id: str
    sender_bank: str

    receiver: str
    receiver_id: str
    receiver_bank: str

    account_no: str

    remark: str
    session_id: str


class SendTransactionModel(BaseModel):
    amount: float

    from_main_pipeline: Optional[str]
    from_branch_pipeline: Optional[str]

    to_main_pipeline: Optional[str]
    to_branch_pipeline: Optional[str]

    receiver: Optional[str]
    receiver_id: Optional[str]
    receiver_bank: Optional[str]

    account_no: Optional[str]

    remark: Optional[str]


class TransactionsResponse(Response):
    transactions: list[TransactionModel]


class TransactionResponse(Response):
    transaction: TransactionModel
