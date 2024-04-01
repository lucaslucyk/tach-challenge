from typing import Any, Dict

from petisco.base.domain.errors.default_http_error_map import (
    DEFAULT_HTTP_ERROR_MAP,
)
from petisco.base.misc.result_mapper import ResultMapper
from petisco_sanic.extra.sanic.controller.sanic_failure_handler import (
    sanic_failure_handler,
)
from petisco_sanic.extra.sanic.controller.sanic_success_handler import (
    sanic_success_handler,
)


class SanicResultMapper:
    @staticmethod
    def default() -> ResultMapper:
        return ResultMapper(
            error_map=DEFAULT_HTTP_ERROR_MAP,
            success_handler=sanic_success_handler,
            failure_handler=sanic_failure_handler,
        )

    @staticmethod
    def from_config(config: Dict[str, Any]) -> ResultMapper:
        error_map = getattr(config, "error_map", DEFAULT_HTTP_ERROR_MAP)
        error_map = {**DEFAULT_HTTP_ERROR_MAP, **error_map}
        return ResultMapper(
            error_map=error_map,
            success_handler=getattr(
                config, "success_handler", sanic_success_handler
            ),
            failure_handler=getattr(
                config, "failure_handler", sanic_failure_handler
            ),
        )
