from abc import abstractmethod
from typing import Any, Dict, Union

from meiga import AnyResult, NotImplementedMethodError

from petisco.base.application.controller.controller import Controller
from petisco.base.misc.result_mapper import ResultMapper
from petisco_sanic.extra.sanic.controller.sanic_result_mapper import SanicResultMapper


class SanicController(Controller):
    @staticmethod
    def get_default_mapper() -> ResultMapper:
        return SanicResultMapper.default()

    @staticmethod
    def get_config_mapper(config: Dict[str, Any]) -> ResultMapper:
        return SanicResultMapper.from_config(config)

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> AnyResult:
        return NotImplementedMethodError

    @classmethod
    def responses(cls) -> Union[Dict[Union[int, str], Dict[str, Any]], None]:
        controller = cls()

        if not hasattr(controller, "Config"):
            return None

        config = getattr(controller, "Config")
        if not hasattr(config, "error_map"):
            return None

        expected_responses = {
            http_error.status_code: {"description": http_error.detail}
            for http_error in config.error_map.values()
        }
        return expected_responses
