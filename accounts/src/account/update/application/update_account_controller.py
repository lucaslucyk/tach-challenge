from meiga import Error, Result
from petisco import AggregateNotFoundError, Container, DomainEventBus
from petisco.base.domain.errors.defaults.already_exists import AlreadyExists
from accounts.src.account.update.application.account_updater import AccountUpdater
from petisco_sanic.extra.sanic import AsyncSanicController
from accounts.src.account.create.application.account_creator import (
    AccountCreator,
)
from petisco import HttpError
from accounts.src.account.shared.domain.account import Account
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)


class UpdateAccountController(AsyncSanicController):

    class Config:
        error_map = {
            AlreadyExists: HttpError(
                status_code=409,
                detail="There is already an account with that alias"
            ),
            AggregateNotFoundError: HttpError(
                status_code=404, detail="Account not found"
            ),
        }

    async def execute(self, account: Account) -> Result[Account, Error]:
        account_creator = AccountUpdater(
            repository=Container.get(
                AsyncCrudRepository, alias="account_repository"
            ),
            domain_event_bus=Container.get(
                DomainEventBus,
                alias="account_event_bus",
            ),
        )
        return await account_creator.execute(account=account)
