from accounts.api.app import app as sanic_app
from accounts.config import settings

if __name__ == "__main__":
    sanic_app.run(
        host=settings.sanic_app_host,
        port=settings.sanic_app_port,
        dev=True,
    )
