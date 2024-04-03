from meiga import Error, Result
from petisco import DomainEventBus, AsyncUseCase
from accounts.src.transaction.shared.domain.transaction import TransactionStatus
from transactions.src.transaction.shared.domain.events import (
    TransactionRejected,
)
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)
from transactions.src.transaction.shared.domain.transaction import Transaction


class TransactionRejecter(AsyncUseCase):
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

        # ensure rejected
        transaction.status = TransactionStatus.REJECTED

        result = await self.repository.update(transaction)
        if result.is_failure:
            return result

        transaction.record(
            TransactionRejected(data=transaction.model_dump(mode="json"))
        )
        self.domain_event_bus.publish(transaction.pull_domain_events())
        return result
