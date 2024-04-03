from petisco import Builder, Dependency
from petisco.extra.rabbitmq import get_rabbitmq_message_dependencies
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)
from transactions import (
    APPLICATION_NAME,
    ORGANIZATION,
    ACCOUNTS_ORGANIZATION,
    ACCOUNTS_APP_NAME,
)
from transactions.src.transaction.shared.infrastructure.document.transaction_repository import (
    DocumentTransactionRepository,
)


def dependencies_provider() -> list[Dependency]:
    repositories = [
        Dependency(
            AsyncCrudRepository,
            alias="transaction_repository",
            envar_modifier="ACCOUNT_REPOSITORY_TYPE",
            builders={
                "default": Builder(DocumentTransactionRepository),
            },
        )
    ]

    transaction_message_dependencies = get_rabbitmq_message_dependencies(
        organization=ORGANIZATION,
        service=APPLICATION_NAME,
        alias="transaction_event_bus",
    )
    account_message_dependencies = get_rabbitmq_message_dependencies(
        organization=ACCOUNTS_ORGANIZATION,
        service=ACCOUNTS_APP_NAME,
        alias="account_message_consummer",
    )

    dependencies = (
        repositories
        + transaction_message_dependencies
        + account_message_dependencies
    )
    return dependencies
