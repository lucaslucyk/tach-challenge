from meiga import Error, Result, Success
from petisco import unwrap_result_handler
from petisco_sanic.extra.sanic import SanicController

from accounts import APPLICATION_VERSION
from accounts.config import settings


class HealthCheckController(SanicController):
    class Config:
        success_handler: unwrap_result_handler

    def execute(self) -> Result[dict, Error]:
        healthcheck = {
            "app_name": settings.application_name,
            "app_version": APPLICATION_VERSION,
        }
        return Success(healthcheck)
