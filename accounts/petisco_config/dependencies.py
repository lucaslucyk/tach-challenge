from petisco import Builder, CrudRepository, Dependency, InmemoryCrudRepository
from petisco.extra.rabbitmq import get_rabbitmq_message_dependencies
from accounts import APPLICATION_NAME, ORGANIZATION
from accounts.src.account.shared.domain.account import Account
from accounts.src.account.shared.infrastructure.document.account_repository import (
    DocumentAccountRepository,
)
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
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

    message_dependencies = get_rabbitmq_message_dependencies(
        ORGANIZATION, APPLICATION_NAME
    )

    dependencies = repositories + message_dependencies # + app_services
    return dependencies
