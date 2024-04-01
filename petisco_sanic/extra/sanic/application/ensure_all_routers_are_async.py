from loguru import logger
from sanic.app import Sanic
from sanic.router import Route


def is_async_callable(route: Route) -> bool:
    handler = route.handler
    import asyncio

    return asyncio.iscoroutinefunction(handler)


def ensure_all_routers_are_async(app: Sanic) -> None:
    for route in app.router.routes:
        if isinstance(route, Route):
            if not is_async_callable(route):
                logger.error(
                    f"Router with {route.path} is not using async definition"
                )
                raise SystemError(
                    f"Router of {route.path} is not using async definition"
                )
