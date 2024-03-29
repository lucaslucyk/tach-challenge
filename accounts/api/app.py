from beanie import init_beanie
from sanic.app import Sanic
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from accounts.api.v1.routes.accounts import blueprint as accounts_blueprint
from accounts.config import TachConfig, settings
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

app.ext.openapi.describe(
    "Accounts API",
    version="0.1.0",
    description="Create, Read, Update and Delete Accounts.",
)
app.ext.openapi.contact(name="Lucas Lucyk", email="lucaslucyk@gmail.com")
app.ext.openapi.license(
    name="View the license",
    url="https://github.com/lucaslucyk/tach-challenge/blob/main/LICENSE",
)
