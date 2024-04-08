import pytest
from sanic_testing.manager import TestManager
from petisco_sanic.base.testing.assert_http import assert_http


@pytest.mark.acceptance
class TestGetHealthcheck:

    def should_success(
        self,
        client_app_manager: TestManager,
        api_version_prefix: str,
    ):
        request, response = client_app_manager.test_client.get(
            f"{api_version_prefix}/healthcheck",
        )
        assert_http(response, 200)
