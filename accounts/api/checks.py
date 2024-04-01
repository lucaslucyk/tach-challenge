from sanic.response import json as json_response
from sanic.blueprints import Blueprint
from sanic.request import Request
from accounts.src.checks.application.healthcheck_controller import (
    HealthCheckController,
)

blueprint = Blueprint("healthcheck", version=1)


@blueprint.get("/")
async def healtcheck(request: Request):
    result = HealthCheckController().execute()
    return json_response(result.value)
