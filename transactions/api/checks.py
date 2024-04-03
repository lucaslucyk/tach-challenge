from sanic.response import json as json_response
from sanic.blueprints import Blueprint
from sanic.request import Request
from transactions.src.checks.application.healthcheck_controller import (
    HealthCheckController,
)

blueprint = Blueprint("healthcheck", version=1)


@blueprint.get("/")
async def healthcheck(request: Request):
    result = HealthCheckController().execute()
    if result.is_failure:
        result.transform()
    return json_response(result.value)
