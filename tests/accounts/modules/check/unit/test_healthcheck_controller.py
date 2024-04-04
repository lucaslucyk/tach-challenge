import pytest
from petisco_sanic.extra.sanic import as_sanic
from accounts.src.checks.application.healthcheck_controller import (
    HealthCheckController,
)


@pytest.mark.unit
class TestUnitHealthcheck:
    def should_success(self):
        result = HealthCheckController().execute()
        result = as_sanic(result)
        assert isinstance(result, dict)
