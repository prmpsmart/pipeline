from .model import *


class User(Model):
    def __init__(
        self,
        models: "Users",
        *,
        id: str,
        created_timestamp: int,
        full_name: str,
        email: str,
        password: str,
        phone_number: str = "",
        profile_image: str = "",
        **kwargs
    ) -> None:
        super().__init__(
            models,
            **kwargs,
        )

        self.id = id
        self.created_timestamp = created_timestamp
        self.full_name = full_name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.profile_image = profile_image


class Users(Models):
    model_class = User


Users = Users()
