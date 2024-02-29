from .model import *


class MainPipeline(Model):
    def __init__(
        self,
        models: "MainPipelines",
        *,
        id: str,
        created_timestamp: int,
        name: str,
        email: str,
        percentage: float,
        deleted: bool = False,
        deleted_timestamp: int = 0,
        **kwargs
    ) -> None:
        super().__init__(
            models,
            **kwargs,
        )

        self.id = id
        self.created_timestamp = created_timestamp
        self.name = name
        self.email = email
        self.percentage = percentage
        self.deleted = deleted
        self.deleted_timestamp = deleted_timestamp


class MainPipelines(Models):
    model_class = MainPipeline


MainPipelines = MainPipelines()
