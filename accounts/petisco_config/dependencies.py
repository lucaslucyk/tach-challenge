from petisco import Builder, Dependency
from petisco.extra.rabbitmq import get_rabbitmq_message_dependencies
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)
from accounts import (
    APPLICATION_NAME,
    ORGANIZATION,
    TRANSACTIONS_ORGANIZATION,
    TRANSACTIONS_APP_NAME,
)
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
            },
        )
    ]

    account_message_dependencies = get_rabbitmq_message_dependencies(
        organization=ORGANIZATION,
        service=APPLICATION_NAME,
        alias="account_event_bus",
    )
    transaction_message_dependencies = get_rabbitmq_message_dependencies(
        organization=TRANSACTIONS_ORGANIZATION,
        service=TRANSACTIONS_APP_NAME,
        alias="transaction_message_consummer",
    )

    dependencies = (
        repositories
        + account_message_dependencies
        + transaction_message_dependencies
    )
    return dependencies
