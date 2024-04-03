from typing import List, Optional, Tuple
from meiga import Error, Result
from petisco import Container
from petisco_sanic.extra.sanic import AsyncSanicController
from transactions.src.transaction.shared.domain.transaction import Transaction
from transactions.src.transaction.retrieve_all.application.all_transactions_retriever import (
    AllTransactionsRetriever,
)
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)


class RetrieveAllTransactionsController(AsyncSanicController):
    async def execute(
        self,
        skip: int = 0,
        limit: int = 100,
        sort: Optional[List[Tuple[str, int]]] = None,
    ) -> Result[list[Transaction], Error]:
        return await AllTransactionsRetriever(
            repository=Container.get(
                AsyncCrudRepository, alias="transaction_repository"
            )
        ).execute(skip=skip, limit=limit, sort=sort)
