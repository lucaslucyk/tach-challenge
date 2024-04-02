from typing import List, Optional, Tuple
from meiga import Error, Result, Success
from petisco import AsyncUseCase
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)
from accounts.src.account.shared.domain.account import Account


class AllAccountsRetriever(AsyncUseCase):
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
    ) -> Result[list[Account], Error]:
        accounts = await self.repository.retrieve_all(
            skip=skip,
            limit=limit,
            sort=sort,
        )
        accounts = accounts.unwrap_or_return()
        return Success(accounts)
