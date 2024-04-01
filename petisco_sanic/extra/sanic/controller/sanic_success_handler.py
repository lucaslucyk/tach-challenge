from typing import Any, Dict
from meiga import AnyResult

from petisco_sanic.extra.sanic.controller.sanic_default_response import (
    SANIC_DEFAULT_RESPONSE,
)


def sanic_success_handler(result: AnyResult) -> Dict[str, Any]:
    try:
        response = (
            SANIC_DEFAULT_RESPONSE
            if result.value is True
            else {"result": result.value}
        )
    except Exception:  # noqa
        response = SANIC_DEFAULT_RESPONSE

    return response
