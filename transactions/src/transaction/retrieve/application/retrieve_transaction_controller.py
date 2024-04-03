from meiga import Error, Result
from petisco import AggregateNotFoundError, Container, Uuid
from transactions.src.transaction.retrieve.application.transaction_retriever import (
    TransactionRetriever,
)
from petisco_sanic.extra.sanic import AsyncSanicController
from petisco import HttpError
from transactions.src.transaction.shared.domain.transaction import Transaction
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)


class RetrieveTransactionController(AsyncSanicController):

    class Config:
        error_map = {
            AggregateNotFoundError: HttpError(
                status_code=404, detail="Transaction not found"
            ),
        }

    async def execute(self, aggregate_id: Uuid) -> Result[Transaction, Error]:
        retriever = TransactionRetriever(
            repository=Container.get(
                AsyncCrudRepository, alias="transaction_repository"
            ),
        )
        return await retriever.execute(aggregate_id)
