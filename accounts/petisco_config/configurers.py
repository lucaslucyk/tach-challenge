from loguru import logger
from meiga import BoolResult, isSuccess
from petisco import DomainEvent # ApplicationConfigurer, databases
from petisco.extra.rabbitmq import RabbitMqConfigurer
from petisco.base.domain.message.domain_event_subscriber import DomainEventSubscriber
# from accounts.src.transaction.shared.domain.events import TransactionCreated
from accounts.src.account.shared.domain.events import AccountCreated


# Define RabbitMQ configurers  
class LogOnAccountCreated(DomainEventSubscriber):
    def subscribed_to(self) -> list[type[DomainEvent]]:
        logger.info("Subscribed to AccountCreated!")
        return [AccountCreated]

    def handle(self, domain_event: AccountCreated) -> BoolResult:
        logger.info("Subscribed to AccountCreated!")
        print("AccountCreated: ", domain_event)
        return isSuccess


# configurers = [DatabasesConfigurer()]
configurers = [
    RabbitMqConfigurer(
        subscribers=[LogOnAccountCreated],
        # configurer_alias="account_message_consummer",
        alias="account_event_bus",
    )
]
