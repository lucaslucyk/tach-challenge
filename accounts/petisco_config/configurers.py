# import asyncio
import anyio
from beanie import init_beanie
from loguru import logger
from meiga import AnyResult, BoolResult, Success
from petisco import DomainEvent
from petisco.extra.rabbitmq import RabbitMqConfigurer
from petisco.base.domain.message.domain_event_subscriber import (
    DomainEventSubscriber,
)
from accounts.src.account.move_funds.application.funds_mover_controller import (
    FundsMoverController,
)
from accounts.src.transaction.shared.domain.events import (
    TransactionCreated,
    TransactionUpdated,
)
from accounts.src.transaction.shared.domain.transaction import (
    Transaction,
    TransactionStatus,
)
from accounts.src.account.shared.infrastructure.document.account import (
    DocumentAccount as Account,
)
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from accounts.config import settings


class LogOnTransactionCreated(DomainEventSubscriber):

    def subscribed_to(self) -> list[type[DomainEvent]]:
        return [TransactionCreated, TransactionUpdated]

    async def start_db(self):
        # TODO: add to databases with an AsyncApplication and AsyncConfigurer

        # Create mongo client
        client = AsyncIOMotorClient(settings.mongo_uri)
        db: AsyncIOMotorDatabase = getattr(client, settings.db_name)

        # Init beanie with the Product document class
        await init_beanie(db, document_models=[Account])

    async def process_event(self, transaction: Transaction) -> AnyResult:
        await self.start_db()
        result = await FundsMoverController().execute(transaction)
        if result.is_success:
            logger.info(f"Transaction created result: {result}")

        if result.is_failure:
            logger.error(f"Error on FundsMoverController: {result}")

        return BoolResult(result.is_success)

    def handle(self, domain_event: TransactionCreated) -> BoolResult:
        logger.info("Transaction received!")
        transaction: Transaction = Transaction.create(
            **domain_event.data
        )
        if transaction.status != TransactionStatus.PENDING:
            # nothing to do
            return Success()
        return anyio.run(self.process_event, transaction)


configurers = [
    RabbitMqConfigurer(
        subscribers=[LogOnTransactionCreated],
        alias="transaction_message_consummer",
        # alias="account_event_bus",
    )
]
