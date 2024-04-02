from meiga import AnyResult
from petisco import Container, DomainEventBus
from accounts.src.account.move_funds.application.funds_mover import FundsMover
from accounts.src.transaction.shared.domain.transaction import Transaction
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)
from petisco.base.application.controller.async_controller import AsyncController


class FundsMoverController(AsyncController):

    async def execute(self, transaction: Transaction) -> AnyResult:
        funds_mover = FundsMover(
            repository=Container.get(
                AsyncCrudRepository, alias="account_repository"
            ),
            domain_event_bus=Container.get(
                DomainEventBus,
                alias="account_event_bus",
            ),
        )
        return await funds_mover.execute(transaction)
