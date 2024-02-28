from .model import *


class Transaction(Model):
    def __init__(
        self,
        models: "Transactions",
        *,
        id: str,
        created_timestamp: int,
        type: str,
        amount: float = None,
        status: str = "",
        main_pipeline: str = "",
        branch_pipeline: str = "",
        sender: str = "",
        sender_bank: str = "",
        receiver: str = "",
        receiver_bank: str = "",
        account_no: str = "",
        remark: str = "",
        session_id: str = "",
        **kwargs
    ) -> None:
        super().__init__(
            models,
            **kwargs,
        )

        self.id = id
        self.created_timestamp = created_timestamp
        self.type = type
        self.amount = amount
        self.status = status
        self.main_pipeline = main_pipeline
        self.branch_pipeline = branch_pipeline
        self.sender = sender
        self.sender_bank = sender_bank
        self.receiver = receiver
        self.receiver_bank = receiver_bank
        self.account_no = account_no
        self.remark = remark
        self.session_id = session_id


class Transactions(Models):
    model_class = Transaction


Transactions = Transactions()
