from decouple import config
from pydantic_settings import BaseSettings
from sanic import Config


# TODO: Move to Sanic config?
class Settings(BaseSettings):

    # api url
    root_url: str = config("ROOT_URL", default="http://localhost:8000")
    sanic_app_host: str = config("SANIC_APP_HOST", default="0.0.0.0")
    sanic_app_port: int = int(config("SANIC_APP_PORT", default=8000))
    sanic_app_name: str = config("SANIC_APP_NAME", default="accounts-api")

    # database
    mongo_uri: str = config("MONGO_URI")
    db_name: str = config("DB_NAME", default="tach")

    # message queue
    # rabbitmq_uri: str = config("RABBITMQ_URI")

    # petisco aplication
    organization: str = config("ORGANIZATION", default="tach")
    application_name: str = config("APPLICATION_NAME", default="accounts-app")
    transactions_organization: str = config(
        "TRANSACTIONS_ORGANIZATION", default="tach"
    )
    transactions_app_name: str = config(
        "TRANSACTIONS_APP_NAME", default="transactions-app"
    )

    # application_version: str = config("APPLICATION_VERSION", default="1.0.0")
    # application_last_deploy: str = config("APPLICATION_LAST_DEPLOY", default="1.0.0")
    environment: str = str(config("ENVIRONMENT", default="local")).lower()


class SanicConfig(Config): ...


settings = Settings()
