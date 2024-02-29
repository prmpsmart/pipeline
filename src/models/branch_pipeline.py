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
        self.main_pipeline = main_pipeline
        self.email = email
        self.percentage = percentage
        self.deleted = deleted
        self.deleted_timestamp = deleted_timestamp


class BranchPipelines(Models):
    model_class = BranchPipeline


BranchPipelines = BranchPipelines()
