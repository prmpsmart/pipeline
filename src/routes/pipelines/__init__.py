from fastapi import APIRouter

from ...utils.commons import get_timestamp

from ...models import *
from .api_models import *


pipelines_router = APIRouter(
    prefix="/pipelines",
    tags=["Pipelines"],
)


@pipelines_router.get(
    "/",
    name="Get all main pipelines",
    responses={
        HTTP_200_OK: {
            "model": PipelinesResponse,
            "description": "Pipelines returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid session",
        },
    },
)
async def pipelines(session=get_user_session) -> PipelinesResponse:
    user = session.user
    main_pipelines: list[MainPipeline] = MainPipelines.find(
        dict(
            email=user.email,
            deleted=False,
        )
    )

    pipelines: list[MainPipelineModel] = []

    for main_pipeline in main_pipelines:
        branch_pipelines: list[BranchPipeline] = BranchPipelines.find(
            dict(
                main_pipeline=main_pipeline.name,
                email=user.email,
                deleted=False,
            )
        )
        pipelines.append(
            MainPipelineModel(
                id=main_pipeline.id,
                created_timestamp=main_pipeline.created_timestamp,
                name=main_pipeline.name,
                email=main_pipeline.email,
                percentage=main_pipeline.percentage,
                branches=[
                    BranchPipelineModel(
                        id=branch_pipeline.id,
                        created_timestamp=branch_pipeline.created_timestamp,
                        name=branch_pipeline.name,
                        main_pipeline=branch_pipeline.main_pipeline,
                        email=branch_pipeline.email,
                        percentage=branch_pipeline.percentage,
                    )
                    for branch_pipeline in branch_pipelines
                ],
            )
        )
    return PipelinesResponse(
        detail="Pipelines returned successfully.",
        pipelines=pipelines,
    )


@pipelines_router.post(
    "/",
    name="Create a new main pipeline",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Pipeline created successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid session.",
        },
        HTTP_406_NOT_ACCEPTABLE: {
            "model": Response,
            "description": "Percentage allocation is not acceptable, maximum available allocation is {maximum_availale_allocation}.",
        },
        HTTP_409_CONFLICT: {
            "model": Response,
            "description": "Pipeline with same name already exists.",
        },
    },
)
async def pipelines(req: PostPipeline, session=get_user_session) -> Response:
    user = session.user
    main_pipelines: list[MainPipeline] = MainPipelines.find(
        dict(
            email=user.email,
            deleted=False,
        )
    )

    main_pipelines_names = [main_pipeline.name for main_pipeline in main_pipelines]

    if req.name not in main_pipelines_names:
        total_percentage = sum(
            [main_pipeline.percentage for main_pipeline in main_pipelines]
        )

        if (total_percentage + req.percentage) <= 100.0:
            MainPipelines.create(
                name=req.name,
                email=user.email,
                percentage=req.percentage,
            )
            return Response(detail="Pipeline created successfully.")

        else:
            maximum_availale_allocation = 100.0 - total_percentage
            raise HTTPException(
                HTTP_406_NOT_ACCEPTABLE,
                detail=f"Percentage allocation is not acceptable, maximum available allocation is {maximum_availale_allocation}.",
            )

    else:
        raise HTTPException(
            HTTP_409_CONFLICT,
            detail="Pipeline with same name already exists.",
        )


@pipelines_router.get(
    "/{pipeline}",
    name="Get a main pipeline",
    responses={
        HTTP_200_OK: {
            "model": MainPipelineResponse,
            "description": "Pipeline returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid session.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Main pipeline with the provided name does not eists.",
        },
    },
)
async def pipeline(pipeline: str, session=get_user_session) -> MainPipelineResponse:
    user = session.user
    main_pipeline: MainPipeline = MainPipelines.find_one(
        dict(
            email=user.email,
            name=pipeline,
            deleted=False,
        )
    )

    if main_pipeline:
        branch_pipelines: list[BranchPipeline] = BranchPipelines.find(
            dict(
                main_pipeline=main_pipeline.name,
                email=user.email,
                deleted=False,
            )
        )
        return MainPipelineResponse(
            detail="Pipeline returned successfully.",
            pipeline=MainPipelineModel(
                id=main_pipeline.id,
                created_timestamp=main_pipeline.created_timestamp,
                name=main_pipeline.name,
                email=main_pipeline.email,
                percentage=main_pipeline.percentage,
                branches=[
                    BranchPipelineModel(
                        id=branch_pipeline.id,
                        created_timestamp=branch_pipeline.created_timestamp,
                        name=branch_pipeline.name,
                        main_pipeline=branch_pipeline.main_pipeline,
                        email=branch_pipeline.email,
                        percentage=branch_pipeline.percentage,
                    )
                    for branch_pipeline in branch_pipelines
                ],
            ),
        )

    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Main pipeline with the provided name does not eists.",
        )


@pipelines_router.patch(
    "/{pipeline}",
    name="Update a main pipeline",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Pipeline updated successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid session.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Main pipeline with the provided name does not eists.",
        },
        HTTP_406_NOT_ACCEPTABLE: {
            "model": Response,
            "description": "Percentage allocation is not acceptable, maximum available allocation is {maximum_availale_allocation}.",
        },
    },
)
async def pipeline(
    pipeline: str,
    req: PatchPipeline,
    session=get_user_session,
) -> Response:
    user = session.user
    main_pipelines: list[MainPipeline] = MainPipelines.find(
        dict(
            email=user.email,
            deleted=False,
        )
    )

    main_pipelines_names = [main_pipeline.name for main_pipeline in main_pipelines]

    if pipeline in main_pipelines_names:
        initial_percentages = sum(
            [main_pipeline.percentage for main_pipeline in main_pipelines]
        )
        main_pipeline: MainPipeline = list(
            filter(lambda pl: pl.name == pipeline, main_pipelines)
        )[0]

        new_percentages = (
            initial_percentages - main_pipeline.percentage + req.percentage
        )

        if new_percentages <= 100.0:
            main_pipeline.percentage = req.percentage
            main_pipeline.save()
            return Response(detail="Pipeline updated successfully.")
        else:
            maximum_availale_allocation = 100.0 - (
                initial_percentages - main_pipeline.percentage
            )
            raise HTTPException(
                HTTP_406_NOT_ACCEPTABLE,
                detail=f"Percentage allocation is not acceptable, maximum available allocation is {maximum_availale_allocation}.",
            )

    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Main pipeline with the provided name does not eists.",
        )


@pipelines_router.delete(
    "/{pipeline}",
    name="Delete a main pipeline",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Pipeline deleted successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid session.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Main pipeline with the provided name does not eists.",
        },
    },
)
async def pipeline(pipeline: str, session=get_user_session) -> Response:
    user = session.user
    main_pipeline: MainPipeline = MainPipelines.find_one(
        dict(
            email=user.email,
            name=pipeline,
            deleted=False,
        )
    )
    if main_pipeline:
        main_pipeline.deleted = True
        main_pipeline.deleted_timestamp = get_timestamp()
        main_pipeline.save()

        branch_pipelines: list[BranchPipeline] = BranchPipelines.find(
            dict(
                main_pipeline=main_pipeline.name,
                email=user.email,
                deleted=False,
            )
        )
        for branch_pipeline in branch_pipelines:
            branch_pipeline.deleted = True
            branch_pipeline.deleted_timestamp = get_timestamp()
            branch_pipeline.save()

        return Response(detail="Pipeline deleted successfully.")

    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Main pipeline with the provided name does not eists.",
        )


@pipelines_router.post(
    "/{pipeline}",
    name="Create a branch pipeline",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Branch pipeline created successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid session.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Main pipeline with the provided name does not eists.",
        },
        HTTP_406_NOT_ACCEPTABLE: {
            "model": Response,
            "description": "Percentage allocation is not acceptable, maximum available allocation is {maximum_availale_allocation}.",
        },
        HTTP_409_CONFLICT: {
            "model": Response,
            "description": "Branch pipeline with same name already exists.",
        },
    },
)
async def pipeline(
    pipeline: str,
    req: PostPipeline,
    session=get_user_session,
) -> Response:
    user = session.user
    main_pipeline: MainPipeline = MainPipelines.find_one(
        dict(
            email=user.email,
            name=pipeline,
            deleted=False,
        )
    )
    if main_pipeline:
        branch_pipelines: list[BranchPipeline] = BranchPipelines.find(
            dict(
                main_pipeline=main_pipeline.name,
                email=user.email,
                deleted=False,
            )
        )
        branch_pipelines_names = [
            branch_pipeline.name for branch_pipeline in branch_pipelines
        ]

        if req.name not in branch_pipelines_names:
            total_percentage = sum(
                [branch_pipeline.percentage for branch_pipeline in branch_pipelines]
            )

            if (total_percentage + req.percentage) <= 100.0:
                BranchPipelines.create(
                    name=req.name,
                    main_pipeline=main_pipeline.name,
                    email=user.email,
                    percentage=req.percentage,
                )
                return Response(detail="Branch pipeline created successfully.")

            else:
                maximum_availale_allocation = 100.0 - total_percentage
                raise HTTPException(
                    HTTP_406_NOT_ACCEPTABLE,
                    detail=f"Percentage allocation is not acceptable, maximum available allocation is {maximum_availale_allocation}.",
                )

        else:
            raise HTTPException(
                HTTP_409_CONFLICT,
                detail="Branch pipeline with same name already exists.",
            )

    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Main pipeline with the provided name does not eists.",
        )


@pipelines_router.get(
    "/{pipeline}/{branch}",
    name="Get a branch pipeline",
    responses={
        HTTP_200_OK: {
            "model": BranchPipelineResponse,
            "description": "Branch pipeline returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid session.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Main or branch pipeline with the provided name does not eists.",
        },
    },
)
async def pipeline(
    pipeline: str,
    branch: str,
    session=get_user_session,
) -> BranchPipelineResponse:
    user = session.user
    branch_pipeline: BranchPipeline = BranchPipelines.find_one(
        dict(
            email=user.email,
            name=branch,
            main_pipeline=pipeline,
            deleted=False,
        )
    )
    if branch_pipeline:
        return BranchPipelineResponse(
            detail="Branch pipeline returned successfully.",
            pipeline=BranchPipelineModel(
                id=branch_pipeline.id,
                created_timestamp=branch_pipeline.created_timestamp,
                name=branch_pipeline.name,
                main_pipeline=branch_pipeline.main_pipeline,
                email=branch_pipeline.email,
                percentage=branch_pipeline.percentage,
            ),
        )

    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Main or branch pipeline with the provided name does not eists.",
        )


@pipelines_router.patch(
    "/{pipeline}/{branch}",
    name="Update a branch pipeline",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Branch pipeline updated successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid session.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Main or branch pipeline with the provided name does not eists.",
        },
        HTTP_406_NOT_ACCEPTABLE: {
            "model": Response,
            "description": "Percentage allocation is not acceptable, maximum available allocation is {maximum_availale_allocation}.",
        },
    },
)
async def pipeline(
    pipeline: str,
    branch: str,
    req: PatchPipeline,
    session=get_user_session,
) -> Response:
    user = session.user
    branch_pipelines: list[BranchPipeline] = BranchPipelines.find(
        dict(
            email=user.email,
            main_pipeline=pipeline,
            deleted=False,
        )
    )
    branch_pipelines_names = [
        branch_pipeline.name for branch_pipeline in branch_pipelines
    ]

    if branch in branch_pipelines_names:
        initial_percentages = sum(
            [branch_pipeline.percentage for branch_pipeline in branch_pipelines]
        )
        branch_pipeline: BranchPipeline = list(
            filter(lambda bl: bl.name == branch, branch_pipelines)
        )[0]

        new_percentages = (
            initial_percentages - branch_pipeline.percentage + req.percentage
        )

        if new_percentages <= 100.0:
            branch_pipeline.percentage = req.percentage
            branch_pipeline.save()
            return Response(detail="Pipeline updated successfully.")
        else:
            maximum_availale_allocation = 100.0 - (
                initial_percentages - branch_pipeline.percentage
            )
            raise HTTPException(
                HTTP_406_NOT_ACCEPTABLE,
                detail=f"Percentage allocation is not acceptable, maximum available allocation is {maximum_availale_allocation}.",
            )

    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Main or branch pipeline with the provided name does not eists.",
        )


@pipelines_router.delete(
    "/{pipeline}/{branch}",
    name="Delete a branch pipeline",
    responses={
        HTTP_200_OK: {
            "model": Response,
            "description": "Branch pipeline deleted successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid session.",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Main or branch pipeline with the provided name does not eists.",
        },
    },
)
async def pipeline(
    pipeline: str,
    branch: str,
    session=get_user_session,
) -> Response:
    user = session.user
    branch_pipeline: BranchPipeline = BranchPipelines.find_one(
        dict(
            email=user.email,
            name=branch,
            main_pipeline=pipeline,
            deleted=False,
        )
    )

    if branch_pipeline:
        branch_pipeline.deleted = True
        branch_pipeline.deleted_timestamp = get_timestamp()
        branch_pipeline.save()
        return Response(detail="Pipeline deleted successfully.")

    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Main or branch pipeline with the provided name does not eists.",
        )
