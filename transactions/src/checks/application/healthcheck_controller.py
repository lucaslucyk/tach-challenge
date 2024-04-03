from meiga import Error, Result, Success
from petisco import unwrap_result_handler
from petisco_sanic.extra.sanic import SanicController

from transactions import APPLICATION_NAME, APPLICATION_VERSION


class HealthCheckController(SanicController):
    class Config:
        success_handler: unwrap_result_handler

    def execute(self) -> Result[dict, Error]:
        healthcheck = {
            "app_name": APPLICATION_NAME,
            "app_version": APPLICATION_VERSION,
        }
        return Success(healthcheck)
