from decouple import config
from pydantic_settings import BaseSettings
from sanic import Config


# TODO: Move to Sanic config?
class Settings(BaseSettings):

    # api url
    root_url: str = config("ROOT_URL", default="http://localhost:8000")
    sanic_app_host: str = config("SANIC_APP_HOST", default="0.0.0.0")
    sanic_app_port: int = int(config("SANIC_APP_PORT", default=8000))
    sanic_app_name: str = config("SANIC_APP_NAME", default="transactions-api")

    # database
    mongo_uri: str = config("MONGO_URI")
    db_name: str = config("DB_BANE", default="tach")

    # message queue
    rabbitmq_uri: str = config("RABBITMQ_URI")


class SanicConfig(Config):
    ...


settings = Settings()
