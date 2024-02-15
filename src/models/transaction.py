from .model import *


class Transaction(Model):
    def __init__(
        self,
        models: "Transactions",
        *,
        id: str,
        created_timestamp: int,
        amount: float = None,
        sender: str = "",
        receiver: str = "",
        main_pipeline: str = "",
        branch_pipeline: str = "",
        remark: str = "",
        originating_bank: str = "",
        **kwargs
    ) -> None:
        super().__init__(
            models,
            **kwargs,
        )

        self.id = id
        self.created_timestamp = created_timestamp
        self.amount = amount
        self.sender = sender
        self.receiver = receiver
        self.main_pipeline = main_pipeline
        self.branch_pipeline = branch_pipeline
        self.remark = remark
        self.originating_bank = originating_bank


class Transactions(Models):
    model_class = Transaction


Transactions = Transactions()
