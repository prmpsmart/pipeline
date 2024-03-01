from fastapi import APIRouter
from .utils import *


transactions_router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


@transactions_router.get(
    "/",
    name="Get all user's transactions",
    responses={
        HTTP_200_OK: {
            "model": TransactionsResponse,
            "description": "Transactions returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid session",
        },
    },
)
async def transactions(session=get_user_session) -> TransactionsResponse:
    user = session.user
    users_transactions: list[Transaction] = Transactions.find(
        search_or=[
            dict(sender_id=user.id),
            dict(receiver_id=user.id),
        ]
    )
    return get_transactions_response(
        "Transactions returned successfully.",
        users_transactions,
    )


@transactions_router.get(
    "/{transaction_id}",
    name="Get a user's transaction",
    responses={
        HTTP_200_OK: {
            "model": TransactionResponse,
            "description": "Transaction returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid session",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid transaction id",
        },
    },
)
async def transactions(
    transaction_id: str,
    _=get_user_session,
) -> TransactionResponse:
    if transaction := Transactions.find_child(transaction_id):
        return TransactionResponse(
            detail="Transaction returned successfully.",
            transaction=get_transaction_model(transaction),
        )
    else:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="Invalid transaction id.",
        )


@transactions_router.get(
    "/{pipeline}",
    name="Get a user's  pipeline transaction",
    responses={
        HTTP_200_OK: {
            "model": TransactionsResponse,
            "description": "Pipeline's transactions returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid session",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid transaction id",
        },
    },
)
async def transactions(
    pipeline: str,
    session=get_user_session,
) -> TransactionResponse:
    user = session.user
    users_transactions: list[Transaction] = Transactions.find(
        search_or=[
            dict(sender_id=user.id, from_main_pipeline=pipeline),
            dict(receiver_id=user.id, to_main_pipeline=pipeline),
        ]
    )
    return get_transactions_response(
        "Pipeline's transactions returned successfully.",
        users_transactions,
    )


@transactions_router.get(
    "/{pipeline}/{branch}",
    name="Get a user's  branch transaction",
    responses={
        HTTP_200_OK: {
            "model": TransactionsResponse,
            "description": "Branch's transactions returned successfully.",
        },
        HTTP_401_UNAUTHORIZED: {
            "model": Response,
            "description": "Invalid session",
        },
        HTTP_404_NOT_FOUND: {
            "model": Response,
            "description": "Invalid transaction id",
        },
    },
)
async def transactions(
    pipeline: str,
    branch: str,
    session=get_user_session,
) -> TransactionResponse:
    user = session.user
    users_transactions: list[Transaction] = Transactions.find(
        search_or=[
            dict(
                sender_id=user.id,
                from_main_pipeline=pipeline,
                from_branch_pipeline=branch,
            ),
            dict(
                receiver_id=user.id,
                to_main_pipeline=pipeline,
                to_branch_pipeline=branch,
            ),
        ]
    )
    return get_transactions_response(
        "Branch's transactions returned successfully.",
        users_transactions,
    )
