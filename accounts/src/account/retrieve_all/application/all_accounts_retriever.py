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

    async def execute(self) -> Result[list[Account], Error]:
        accounts = await self.repository.retrieve_all()
        accounts = accounts.unwrap_or_return()
        return Success(accounts)
