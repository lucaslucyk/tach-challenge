from meiga import Error, Result
from petisco import AggregateAlreadyExistError, Container, DomainEventBus
from petisco.base.domain.errors.defaults.already_exists import AlreadyExists
from petisco_sanic.extra.sanic import AsyncSanicController
from transactions.src.transaction.create.application.transaction_creator import (
    TransactionCreator,
)
from petisco import HttpError
from transactions.src.transaction.shared.domain.transaction import Transaction
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)


class CreateTransactionController(AsyncSanicController):

    class Config:
        error_map = {
            AlreadyExists: HttpError(
                status_code=409,
                detail="There is already an transaction with that alias",
            ),
            AggregateAlreadyExistError: HttpError(
                status_code=409,
                detail="There is already an transaction with that ID",
            ),
        }

    async def execute(
        self, transaction: Transaction
    ) -> Result[Transaction, Error]:
        transaction_creator = TransactionCreator(
            repository=Container.get(
                AsyncCrudRepository, alias="transaction_repository"
            ),
            domain_event_bus=Container.get(
                DomainEventBus,
                alias="transaction_event_bus",
            ),
        )
        return await transaction_creator.execute(transaction=transaction)
