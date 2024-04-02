from petisco import Builder, CrudRepository, Dependency, InmemoryCrudRepository
from petisco.extra.rabbitmq import get_rabbitmq_message_dependencies

from petisco.base.domain.message.domain_event_bus import DomainEventBus
from petisco.base.domain.message.message_consumer import MessageConsumer
from petisco.extra.rabbitmq.application.message.bus.rabbitmq_domain_event_bus import (
    RabbitMqDomainEventBus,
)
from petisco.extra.rabbitmq.application.message.configurer.rabbitmq_message_configurer import (
    RabbitMqMessageConfigurer,
)
from petisco.extra.rabbitmq.application.message.consumer.rabbitmq_message_consumer import (
    RabbitMqMessageConsumer,
)

from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)
from accounts import (
    APPLICATION_NAME,
    ORGANIZATION,
    TRANSACTIONS_ORGANIZATION,
    TRANSACTIONS_APP_NAME,
)
from accounts.src.account.shared.domain.account import Account
from accounts.src.account.shared.infrastructure.document.account_repository import (
    DocumentAccountRepository,
)


def dependencies_provider() -> list[Dependency]:
    repositories = [
        Dependency(
            AsyncCrudRepository,
            alias="account_repository",
            envar_modifier="ACCOUNT_REPOSITORY_TYPE",
            builders={
                "default": Builder(DocumentAccountRepository),
                # "memory": Builder(InmemoryCrudRepository[Account]),
            },
        )
    ]
    # app_services = [
    #     Dependency(
    #         AccountLabeler,
    #         envar_modifier="ACCOUNT_LABELER_TYPE",
    #         builders={
    #             "default": Builder(SizeAccountLabeler),
    #             "fake": Builder(FakeAccountLabeler),
    #         },
    #     ),
    # ]

    # message_dependencies = [
    #     Dependency(
    #         DomainEventBus,
    #         alias="account_event_bus",
    #         builders={
    #             "default": Builder(
    #                 RabbitMqDomainEventBus,
    #                 organization=ORGANIZATION,
    #                 service=APPLICATION_NAME,
    #             ),
    #         },
    #         envar_modifier="PETISCO_DOMAIN_EVENT_BUS_TYPE",
    #     ),
    #     Dependency(
    #         MessageConsumer,
    #         alias="account_message_consummer",
    #         builders={
    #             "default": Builder(
    #                 RabbitMqMessageConsumer,
    #                 # organization=TRANSACTIONS_ORGANIZATION,
    #                 # service=TRANSACTIONS_APP_NAME,
    #                 organization=ORGANIZATION,
    #                 service=APPLICATION_NAME,
    #                 max_retries=5,
    #             ),
    #         },
    #         envar_modifier="PETISCO_MESSAGE_CONSUMER_TYPE",
    #     ),
    # ]

    message_dependencies = get_rabbitmq_message_dependencies(
        organization=ORGANIZATION,
        service=APPLICATION_NAME,
        alias="account_event_bus",
    )
    transaction_message_dependencies = get_rabbitmq_message_dependencies(
        organization=ORGANIZATION,
        service=APPLICATION_NAME,
        alias="account_message_consummer",
    )

    dependencies = (
        repositories + message_dependencies + transaction_message_dependencies
    )
    return dependencies
