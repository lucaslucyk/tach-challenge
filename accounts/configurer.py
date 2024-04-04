from sanic.app import Sanic
from accounts.api import checks, accounts
from accounts.cors import add_cors_headers
from accounts.config import SanicConfig, settings


def sanic_configurer() -> Sanic:
    app = Sanic(
        name=settings.application_name,
        config=SanicConfig()
    )
    # add blueprints
    app.blueprint(checks.blueprint, url_prefix="/healthcheck")
    app.blueprint(accounts.blueprint, url_prefix="/accounts")

    # Fill in CORS headers
    app.register_middleware(add_cors_headers, "response")
    # app.before_server_start(setup_database)

    app.ext.openapi.describe(
        settings.application_name,
        version="0.1.0",
        description="Create, Read, Update and Delete Accounts.",
    )
    app.ext.openapi.contact(name="Lucas Lucyk", email="lucaslucyk@gmail.com")
    app.ext.openapi.license(
        name="View the license",
        url="https://github.com/lucaslucyk/tach-challenge/blob/main/LICENSE",
    )

    return app