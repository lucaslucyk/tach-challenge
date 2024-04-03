from loguru import logger
from sanic.app import Sanic
from beanie import init_beanie
from sanic.app import Sanic
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from transactions.config import settings
from transactions.application import application
from transactions.src.transaction.shared.infrastructure.document.transaction import (
    DocumentTransaction as Transaction,
)
application.configure()
app: Sanic = application.get_app()


@app.listener("before_server_start")
async def startup_event(app: Sanic, loop):
    # Create mongo client
    client = AsyncIOMotorClient(settings.mongo_uri)
    db: AsyncIOMotorDatabase = getattr(client, settings.db_name)

    # Init beanie with the Product document class
    await init_beanie(db, document_models=[Transaction])  # type: ignore[arg-type,attr-defined]
    logger.info("Startup complete!")


if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    app.run(
        host="0.0.0.0",
        port=5051,
        dev=False,
    )
