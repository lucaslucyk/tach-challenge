from meiga import BoolResult, Error, Result, isSuccess
from petisco import CrudRepository, DomainEventBus, AsyncUseCase
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)
from accounts.src.account.shared.domain.account import Account


class AccountCreator(AsyncUseCase):
    def __init__(
        self,
        # labeler: AccountLabeler,
        repository: AsyncCrudRepository,
        # domain_event_bus: DomainEventBus,
    ):
        # self.labeler = labeler
        self.repository = repository
        # self.domain_event_bus = domain_event_bus

    async def execute(
        self,
        account: Account,
    ) -> Result[Account, Error]:
        # account = self.labeler.execute(account).unwrap_or_return()
        return await self.repository.save(account)
        
        #return result
        # self.domain_event_bus.publish(account.pull_domain_events())
