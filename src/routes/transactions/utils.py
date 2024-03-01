from ...models import *
from .api_models import *


def get_transaction_model(transaction: Transaction) -> TransactionModel:
    return TransactionModel(
        id=transaction.id,
        created_timestamp=transaction.created_timestamp,
        type=transaction.type,
        amount=transaction.amount,
        status=transaction.status,
        from_main_pipeline=transaction.from_main_pipeline,
        from_branch_pipeline=transaction.from_branch_pipeline,
        to_main_pipeline=transaction.to_main_pipeline,
        to_branch_pipeline=transaction.to_branch_pipeline,
        sender=transaction.sender,
        sender_id=transaction.sender_id,
        sender_bank=transaction.sender_bank,
        receiver=transaction.receiver,
        receiver_id=transaction.receiver_id,
        receiver_bank=transaction.receiver_bank,
        account_no=transaction.account_no,
        remark=transaction.remark,
        session_id=transaction.session_id,
    )


def get_transactions_response(
    detail: str,
    transactions: list[Transaction],
) -> TransactionsResponse:
    return TransactionsResponse(
        detail=detail,
        transactions=[
            get_transaction_model(transaction) for transaction in transactions
        ],
    )
