from ..utils import *
from ..api_models import *


class PipelineModel(BaseModel):
    id: str
    created_timestamp: int
    name: str
    email: str
    percentage: float


class BranchPipelineModel(PipelineModel):
    main_pipeline: str


class MainPipelineModel(PipelineModel):
    branches: list[BranchPipelineModel]


class PipelinesResponse(Response):
    pipelines: list[MainPipelineModel]


class MainPipelineResponse(Response):
    pipeline: MainPipelineModel


class BranchPipelineResponse(Response):
    pipeline: BranchPipelineModel


class PostPipeline(BaseModel):
    name: str
    percentage: float


class PatchPipeline(BaseModel):
    percentage: float
