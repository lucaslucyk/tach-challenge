from petisco import Builder, Dependency
from petisco.extra.rabbitmq import get_rabbitmq_message_dependencies
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)
from accounts.src.account.shared.infrastructure.document.account_repository import (
    DocumentAccountRepository,
)
from accounts.config import settings


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
        organization=settings.organization,
        service=settings.application_name,
        alias="account_event_bus",
    )
    transaction_message_dependencies = get_rabbitmq_message_dependencies(
        organization=settings.transactions_organization,
        service=settings.transactions_app_name,
        alias="transaction_message_consummer",
    )

    dependencies = (
        repositories
        + account_message_dependencies
        + transaction_message_dependencies
    )
    return dependencies
