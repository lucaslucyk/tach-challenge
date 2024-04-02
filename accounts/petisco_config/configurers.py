# import asyncio
import anyio
from beanie import init_beanie
from loguru import logger
from meiga import AnyResult, BoolResult
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
from accounts.src.transaction.shared.domain.transaction import Transaction
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

    async def process_event(
        self, domain_event: TransactionCreated
    ) -> AnyResult:
        await self.start_db()

        domain_transaction = Transaction.create(
            source_account_id=domain_event.data.get("source_account_id", None),
            target_account_id=domain_event.data.get("target_account_id", None),
            symbol=domain_event.data.get("symbol", None),
            amount=domain_event.data.get("amount", None),
            aggregate_id=domain_event.data.get("aggregate_id", None),
        )

        result = await FundsMoverController().execute(domain_transaction)
        if result.is_success:
            logger.info(f"Transaction created result: {result}")

        if result.is_failure:
            logger.error(f"Error on FundsMoverController: {result}")

        return BoolResult(result.is_success)

    def handle(self, domain_event: TransactionCreated) -> BoolResult:
        logger.info("Transaction received!")
        return anyio.run(self.process_event, domain_event)


configurers = [
    RabbitMqConfigurer(
        subscribers=[LogOnTransactionCreated],
        alias="transaction_message_consummer",
        # alias="account_event_bus",
    )
]
