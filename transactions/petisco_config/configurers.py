# import asyncio
from typing import Union
import anyio
from beanie import init_beanie
from loguru import logger
from meiga import AnyResult, BoolResult, Success
from petisco import DomainEvent
from petisco.extra.rabbitmq import RabbitMqConfigurer
from petisco.base.domain.message.domain_event_subscriber import (
    DomainEventSubscriber,
)

from transactions.src.transaction.shared.domain.transaction import Transaction
from transactions.src.account.shared.domain.events import (
    FundsMoved,
    AccountNotFound,
    AccountNotAvailable,
    SymbolError,
)
from transactions.src.transaction.approve.application.approve_transaction_controller import (
    ApproveTransactionController,
)
from transactions.src.transaction.reject.application.reject_transaction_controller import (
    RejectTransactionController,
)
from transactions.src.transaction.shared.infrastructure.document.transaction import (
    DocumentTransaction
)
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from transactions.config import settings


class LogOnAccountCreated(DomainEventSubscriber):

    def subscribed_to(self) -> list[type[DomainEvent]]:
        return [FundsMoved, AccountNotFound, AccountNotAvailable, SymbolError]

    async def start_db(self):
        # TODO: add to databases with an AsyncApplication and AsyncConfigurer

        # Create mongo client
        client = AsyncIOMotorClient(settings.mongo_uri)
        db: AsyncIOMotorDatabase = getattr(client, settings.db_name)

        # Init beanie with the Product document class
        await init_beanie(db, document_models=[DocumentTransaction])

    async def process_approve_event(
        self, transaction: Transaction
    ) -> AnyResult:
        await self.start_db()

        result = await ApproveTransactionController().execute(transaction)
        if result.is_success:
            logger.info(f"Transaction approved result: {result}")

        if result.is_failure:
            logger.error(f"Transaction approved error: {result}")

        return BoolResult(result.is_success)

    async def process_reject_event(self, transaction: Transaction) -> AnyResult:
        result = await RejectTransactionController().execute(transaction)
        if result.is_success:
            logger.info(f"Transaction rejected result: {result}")

        if result.is_failure:
            logger.error(f"Transaction rejected error: {result}")

        return BoolResult(result.is_success)

    def handle(
        self,
        domain_event: Union[
            FundsMoved, AccountNotFound, AccountNotAvailable, SymbolError
        ],
    ) -> BoolResult:
        logger.info("Domain event received!")
        transaction: Transaction = Transaction.create(**domain_event.trigger)
        event_kind = domain_event.get_message_name()
        match event_kind:
            case 'funds.moved':
                logger.info(f"Transaction created event: {domain_event}")
                return anyio.run(self.process_approve_event, transaction)
            case 'account.not.found' | 'account.not.available' | 'symbol.error':
                logger.info(f"Transaction rejected event: {domain_event}")
                return anyio.run(self.process_reject_event, transaction)
            case _:
                logger.error(f"Unknown domain event: {domain_event}")

        # nothing to do
        return Success()


configurers = [
    RabbitMqConfigurer(
        subscribers=[LogOnAccountCreated],
        alias="account_message_consummer",
        # alias="transaction_event_bus",
    )
]
