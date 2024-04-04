from petisco import Container
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)
from accounts.src.account.shared.domain.account import Account
from tests.accounts.mothers.account_mother import AccountMother


class AccountRepositoryMother:
    @staticmethod
    async def empty():
        repository = Container.get(
            AsyncCrudRepository, alias="account_repository"
        )
        await repository.clear()
        return repository

    @staticmethod
    async def with_account(account: Account = AccountMother.any()):
        repository = await AccountRepositoryMother.empty()
        await repository.save(account)
        return repository
