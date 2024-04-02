from typing import List, Optional, Tuple
from meiga import Error, Result
from petisco import Container
from petisco_sanic.extra.sanic import AsyncSanicController
from accounts.src.account.shared.domain.account import Account
from accounts.src.account.retrieve_all.application.all_accounts_retriever import (
    AllAccountsRetriever,
)
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)


class RetrieveAllAccountsController(AsyncSanicController):
    async def execute(
        self,
        skip: int = 0,
        limit: int = 100,
        sort: Optional[List[Tuple[str, int]]] = None,
    ) -> Result[list[Account], Error]:
        return await AllAccountsRetriever(
            repository=Container.get(
                AsyncCrudRepository, alias="account_repository"
            )
        ).execute(skip=skip, limit=limit, sort=sort)
