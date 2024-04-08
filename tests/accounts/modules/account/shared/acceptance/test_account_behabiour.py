import pytest
from typing import Any, Tuple
from petisco_sanic.base.testing.assert_http import assert_http
from sanic_testing import TestManager
from sanic_testing.testing import TestingResponse
from tests.accounts.mothers.account_json_mother import AccountJsonMother
from tests.accounts.mothers.account_repository_mother import (
    AccountRepositoryMother,
)
from tests.conftest import pytest_mark_asyncio


# @pytest.mark.acceptance
@pytest.mark.acceptance
@pytest_mark_asyncio(scope="session")
class TestAccountBehaviour:

    async def async_setup(self):
        await AccountRepositoryMother.empty()

    async def should_success_on_complete_account_execution(
        self,
        client_app_manager: TestManager,
        api_version_prefix: str,
    ):
        await self.async_setup()

        account_json = AccountJsonMother.any()
        account_id = account_json.get("id")

        response: TestingResponse = None
        _, response = await client_app_manager.asgi_client.post(
            f"{api_version_prefix}/accounts", json=account_json
        )
        assert_http(response, 201)

        _, response = await client_app_manager.asgi_client.get(
            f"{api_version_prefix}/accounts/{account_id}"
        )
        assert_http(response, 200)
        payload = response.json

        payload.pop("created_at")
        assert payload == account_json

        account_json["name"] = "New name"
        _, response = await client_app_manager.asgi_client.patch(
            f"{api_version_prefix}/accounts", json=account_json
        )
        assert_http(response, 200)

        _, response = await client_app_manager.asgi_client.delete(
            f"{api_version_prefix}/accounts/{account_id}"
        )
        assert_http(response, 200)

        _, response = await client_app_manager.asgi_client.get(
            f"{api_version_prefix}/accounts/{account_id}"
        )
        assert_http(response, 404)

    # TODO
    # def should_success_when_creates_several_accounts_and_list_them(self, client_app):
    #     expected_accounts = 5
    #     for _ in range(expected_accounts):
    #         client_app.post("/account", json=AccountJsonMother.random())
    #
    #     response = client_app.get(f"/accounts")
    #     assert_http(response, 200)
    #     assert len(response.json()) == expected_accounts
