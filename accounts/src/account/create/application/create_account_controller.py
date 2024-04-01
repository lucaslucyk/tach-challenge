from meiga import Error, Result
from petisco import Container  # , CrudRepository, DomainEventBus
from petisco_sanic.extra.sanic import AsyncSanicController
from accounts.src.account.create.application.account_creator import (
    AccountCreator,
)
from accounts.src.account.shared.domain.account import Account
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)


class CreateAccountController(AsyncSanicController):
    async def execute(self, account: Account) -> Result[Account, Error]:
        # repository = Container.get(CrudRepository, alias="account_repository")
        account_creator = AccountCreator(
            # labeler=Container.get(AccountLabeler),
            repository=Container.get(
                AsyncCrudRepository, alias="account_repository"
            ),
            # domain_event_bus=Container.get(DomainEventBus),
        )
        return await account_creator.execute(account=account)
