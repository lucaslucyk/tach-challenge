from sanic.app import Sanic
from accounts import APPLICATION_NAME, ENVIRONMENT
from accounts.api import checks, accounts
from accounts.cors import add_cors_headers
from accounts.config import SanicConfig, settings
# from loguru import logger
# from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
# from beanie import init_beanie
# from accounts.src.account.shared.infrastructure.document.account import (
#     DocumentAccount as Account,
# )

# async def setup_database(app: Sanic, loop):
# # Create mongo client
# client = AsyncIOMotorClient(settings.mongo_uri)
# db: AsyncIOMotorDatabase = getattr(client, settings.db_name)

# # Init beanie with the Product document class
# await init_beanie(db, document_models=[Account])  # type: ignore[arg-type,attr-defined]
# logger.info("Startup complete!")


def sanic_configurer() -> Sanic:
    app = Sanic(
        name=APPLICATION_NAME,
        config=SanicConfig()
    )
    # add blueprints
    app.blueprint(checks.blueprint, url_prefix="/checks")
    app.blueprint(accounts.blueprint, url_prefix="/accounts")

    # Fill in CORS headers
    app.register_middleware(add_cors_headers, "response")
    # app.before_server_start(setup_database)

    return app