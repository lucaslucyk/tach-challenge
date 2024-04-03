from meiga import Error, Result
from petisco import AggregateNotFoundError, Container, DomainEventBus
from petisco.base.domain.errors.defaults.already_exists import AlreadyExists
from transactions.src.transaction.approve.application.transaction_approver import (
    TransactionApprover,
)
from petisco_sanic.extra.sanic import AsyncSanicController
from petisco import HttpError
from transactions.src.transaction.shared.domain.transaction import Transaction
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)


class ApproveTransactionController(AsyncSanicController):

    class Config:
        error_map = {
            AggregateNotFoundError: HttpError(
                status_code=404, detail="Transaction not found"
            ),
        }

    async def execute(
        self, transaction: Transaction
    ) -> Result[Transaction, Error]:
        transaction_creator = TransactionApprover(
            repository=Container.get(
                AsyncCrudRepository, alias="transaction_repository"
            ),
            domain_event_bus=Container.get(
                DomainEventBus,
                alias="transaction_event_bus",
            ),
        )
        return await transaction_creator.execute(transaction=transaction)
