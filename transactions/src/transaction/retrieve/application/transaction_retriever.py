from meiga import Error, Result
from petisco import AsyncUseCase, Uuid
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)
from transactions.src.transaction.shared.domain.transaction import Transaction


class TransactionRetriever(AsyncUseCase):
    def __init__(self, repository: AsyncCrudRepository):
        self.repository = repository

    async def execute(self, aggregate_id: Uuid) -> Result[Transaction, Error]:
        return await self.repository.retrieve(aggregate_id)
