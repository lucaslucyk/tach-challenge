from meiga import Error, Result
from petisco import DomainEventBus, AsyncUseCase, Uuid
from accounts.src.account.shared.domain.events import AccountDeleted
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)
from accounts.src.account.shared.domain.account import Account


class AccountDeleter(AsyncUseCase):
    def __init__(
        self,
        repository: AsyncCrudRepository,
        domain_event_bus: DomainEventBus,
    ):
        self.repository = repository
        self.domain_event_bus = domain_event_bus

    async def execute(
        self,
        aggregate_id: Uuid
    ) -> Result[Account, Error]:
        result = await self.repository.remove(aggregate_id)
        if result.is_failure:
            return result
        
        account: Account = result.value
        account.record(AccountDeleted(data=account.model_dump(mode="json")))
        self.domain_event_bus.publish(account.pull_domain_events())
        return result
