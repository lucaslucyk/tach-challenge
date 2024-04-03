from typing import List, Optional, Tuple
from meiga import Error, Result, Success
from petisco import AsyncUseCase
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)
from transactions.src.transaction.shared.domain.transaction import Transaction


class AllTransactionsRetriever(AsyncUseCase):
    def __init__(
        self,
        repository: AsyncCrudRepository,
    ):
        self.repository = repository

    async def execute(
        self,
        skip: int = 0,
        limit: int = 100,
        sort: Optional[List[Tuple[str, int]]] = None,
    ) -> Result[list[Transaction], Error]:
        transactions = await self.repository.retrieve_all(
            skip=skip,
            limit=limit,
            sort=sort,
        )
        transactions = transactions.unwrap_or_return()
        return Success(transactions)
