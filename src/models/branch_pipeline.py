from .model import *


class BranchPipeline(Model):
    def __init__(
        self,
        models: "BranchPipelines",
        *,
        id: str,
        created_timestamp: int,
        name: str,
        main_pipeline: str,
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
        self.name = name
        self.main_pipeline = main_pipeline
        self.email = email
        self.balance = balance


class BranchPipelines(Models):
    model_class = BranchPipeline


BranchPipelines = BranchPipelines()
