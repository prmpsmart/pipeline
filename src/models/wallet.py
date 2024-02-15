from .model import *


class Wallet(Model):
    def __init__(
        self,
        models: "Wallets",
        *,
        id: str,
        created_timestamp: int,
        email: str,
        balance: float,
        **kwargs
    ) -> None:
        super().__init__(
            models,
            **kwargs,
        )

        self.id = id
        self.created_timestamp = created_timestamp
        self.email = email
        self.balance = balance


class Wallets(Models):
    model_class = Wallet


Wallets = Wallets()
