from meiga import Error, Result
from petisco import AsyncUseCase, Uuid
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)
from accounts.src.account.shared.domain.account import Account


class AccountRetriever(AsyncUseCase):
    def __init__(
        self,
        repository: AsyncCrudRepository,
        # domain_event_bus: DomainEventBus,
    ):
        self.repository = repository
        # self.domain_event_bus = domain_event_bus

    async def execute(self, aggregate_id: Uuid) -> Result[Account, Error]:
        return await self.repository.retrieve(aggregate_id)
