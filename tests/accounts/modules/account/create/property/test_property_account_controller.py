from sanic.exceptions import HTTPException
from petisco_sanic.extra.sanic import as_sanic
from accounts.src.account.create.application.create_account_controller import (
    CreateAccountController,
)
from tests.accounts.mothers.account_mother import AccountMother
from tests.accounts.mothers.account_repository_mother import (
    AccountRepositoryMother,
)
from tests.conftest import pytest_mark_asyncio


@pytest_mark_asyncio(scope="session")
class TestPropertyCreateAccountController:
    async def async_setup(self):
        await AccountRepositoryMother.empty()

    async def async_teardown(self):
        await AccountRepositoryMother.empty()

    async def should_construct_and_execute(self, config_app):
        await self.async_setup()
        task = AccountMother.random(
            name="fake-name", alias="fake.property.alias"
        )
        try:
            result = await CreateAccountController().execute(task)
            result = as_sanic(result)
            assert isinstance(result, dict)
        except HTTPException as exc:
            assert exc.status_code == 400
        finally:
            await self.async_teardown()
