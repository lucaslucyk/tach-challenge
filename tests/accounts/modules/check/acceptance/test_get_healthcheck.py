import pytest
from sanic_testing.manager import TestManager
from petisco_sanic.base.testing.assert_http import assert_http


@pytest.mark.acceptance
class TestGetHealthcheck:

    VERSION = "v1"

    def should_success(self, client_app_manager: TestManager):
        request, response = client_app_manager.test_client.get(
            f"{self.VERSION}/healthcheck",
        )
        assert_http(response, 200)
