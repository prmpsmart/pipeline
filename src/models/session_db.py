from .model import *


class SessionDb(Model):
    def __init__(
        self,
        models: "SessionDbs",
        *,
        id: str,
        created_timestamp: int,
        user_id: str,
        deleted_timestamp: int = 0,
        **kwargs
    ) -> None:
        super().__init__(
            models,
            **kwargs,
        )

        self.id = id
        self.created_timestamp = created_timestamp
        self.user_id = user_id
        self.deleted_timestamp = deleted_timestamp


class SessionDbs(Models):
    model_class = SessionDb


SessionDbs = SessionDbs()
