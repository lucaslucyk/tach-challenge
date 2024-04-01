from typing import Callable
from sanic.app import Sanic
from petisco.base.application.application import Application
from petisco_sanic.extra.sanic.application.ensure_all_routers_are_async import (
    ensure_all_routers_are_async,
)


class SanicApplication(Application):
    sanic_configurer: Callable[[], Sanic]
    ensure_async_routers: bool = False

    def get_app(self) -> Sanic:
        app = self.sanic_configurer()

        if self.ensure_async_routers is True:
            ensure_all_routers_are_async(app)

        return app
