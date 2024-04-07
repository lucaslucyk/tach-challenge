import inspect
from typing import Any, Callable, Optional


class Decorator:

    @staticmethod
    def prepare(method: Callable) -> Callable:
        async def wrapper(instance, *args, **kwargs) -> Optional[Any]:
            async_setup = getattr(instance, "async_setup", None)
            if async_setup:
                at_start = async_setup()
                if inspect.isawaitable(at_start):
                    await at_start

            try:
                # Ejecutamos la función original
                result = method(*args, **kwargs)
                if inspect.isawaitable(result):
                    await result
            except:
                raise
            finally:
                async_teardown = getattr(instance, "async_teardown", None)
                if async_teardown:
                    at_down = async_teardown()
                    if inspect.isawaitable(at_down):
                        await at_down
            return result

        return wrapper
