from accounts.src.account.create.application.create_account_controller import (
    CreateAccountController,
)
from tests.accounts.mothers.account_mother import AccountMother
from tests.accounts.mothers.account_repository_mother import (
    AccountRepositoryMother,
)
from tests.conftest import pytest_mark_asyncio


@pytest_mark_asyncio(scope="session")
class TestCreateAccountController:
    async def setup(self):
        await AccountRepositoryMother.empty()

    # @pytest_mark_asyncio(scope="session")
    async def should_construct_and_execute(self, config_app):
        await self.setup()
        account = AccountMother.any()
        await CreateAccountController().execute(account)
