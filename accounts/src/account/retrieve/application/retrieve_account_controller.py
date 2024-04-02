from meiga import Error, Result
from petisco import AggregateNotFoundError, Container, Uuid
from accounts.src.account.retrieve.application.account_retriever import (
    AccountRetriever,
)
from petisco_sanic.extra.sanic import AsyncSanicController
from petisco import HttpError
from accounts.src.account.shared.domain.account import Account
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)


class RetrieveAccountController(AsyncSanicController):

    class Config:
        error_map = {
            AggregateNotFoundError: HttpError(
                status_code=404, detail="Account not found"
            ),
        }

    async def execute(self, aggregate_id: Uuid) -> Result[Account, Error]:
        retriever = AccountRetriever(
            repository=Container.get(
                AsyncCrudRepository, alias="account_repository"
            ),
        )
        return await retriever.execute(aggregate_id)
