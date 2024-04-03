from meiga import Error, Result
from petisco import DomainEventBus, AsyncUseCase
from transactions.src.transaction.shared.domain.events import TransactionCreated
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)
from transactions.src.transaction.shared.domain.transaction import Transaction


class TransactionCreator(AsyncUseCase):
    def __init__(
        self,
        repository: AsyncCrudRepository,
        domain_event_bus: DomainEventBus,
    ):
        self.repository = repository
        self.domain_event_bus = domain_event_bus

    async def execute(
        self,
        transaction: Transaction,
    ) -> Result[Transaction, Error]:
        result = await self.repository.save(transaction)
        if result.is_failure:
            return result

        transaction.record(
            TransactionCreated(data=result.value.model_dump(mode="json"))
        )
        self.domain_event_bus.publish(transaction.pull_domain_events())
        return result
