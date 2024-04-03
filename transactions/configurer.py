from sanic.app import Sanic
from transactions import APPLICATION_NAME, ENVIRONMENT
from transactions.api import checks, transactions
from transactions.cors import add_cors_headers
from transactions.config import SanicConfig


def sanic_configurer() -> Sanic:
    app = Sanic(
        name=APPLICATION_NAME,
        config=SanicConfig()
    )
    # add blueprints
    app.blueprint(checks.blueprint, url_prefix="/healthcheck")
    app.blueprint(transactions.blueprint, url_prefix="/transactions")

    # Fill in CORS headers
    app.register_middleware(add_cors_headers, "response")
    # app.before_server_start(setup_database)

    app.ext.openapi.describe(
        APPLICATION_NAME,
        version="0.1.0",
        description="Create, Read, Update and Delete Transactions.",
    )
    app.ext.openapi.contact(name="Lucas Lucyk", email="lucaslucyk@gmail.com")
    app.ext.openapi.license(
        name="View the license",
        url="https://github.com/lucaslucyk/tach-challenge/blob/main/LICENSE",
    )

    return app