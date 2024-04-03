from meiga import Error, Result
from petisco import DomainEventBus, AsyncUseCase, Uuid
from transactions.src.transaction.shared.domain.events import TransactionDeleted
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)
from transactions.src.transaction.shared.domain.transaction import Transaction


class TransactionDeleter(AsyncUseCase):
    def __init__(
        self,
        repository: AsyncCrudRepository,
        domain_event_bus: DomainEventBus,
    ):
        self.repository = repository
        self.domain_event_bus = domain_event_bus

    async def execute(self, aggregate_id: Uuid) -> Result[Transaction, Error]:
        result = await self.repository.remove(aggregate_id)
        if result.is_failure:
            return result

        transaction: Transaction = result.value
        transaction.record(
            TransactionDeleted(data=transaction.model_dump(mode="json"))
        )
        self.domain_event_bus.publish(transaction.pull_domain_events())
        return result
