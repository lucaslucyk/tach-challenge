from beanie import init_beanie
from sanic.app import Sanic
from accounts.config import TachConfig, settings
from accounts.api.v1.routes.accounts import blueprint as accounts_blueprint
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from accounts.models.accounts import Account

app = Sanic(settings.sanic_app_name, config=TachConfig())


@app.listener("before_server_start")
async def setup_database(app: Sanic, loop):
    # Create mongo client    
    client = AsyncIOMotorClient(settings.mongo_uri)
    db: AsyncIOMotorDatabase = getattr(client, settings.db_name)
    
    # Init beanie with the Product document class
    await init_beanie(db, document_models=[Account])  # type: ignore[arg-type,attr-defined]
    print("Startup complete!")


# add routes
app.blueprint(
    blueprint=accounts_blueprint,
    url_prefix="/accounts",
    # version=1,
)
