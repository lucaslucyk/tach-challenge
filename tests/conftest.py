import asyncio
import pytest
import pytest_asyncio
from beanie import init_beanie
from sanic_testing.manager import TestManager
from accounts.application import application
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from accounts.config import settings
from accounts.src.account.shared.infrastructure.document.account import (
    DocumentAccount as Account,
)

pytest_mark_asyncio = pytest.mark.asyncio


# pytest_mark_sync causes problem in pytest
def py_test_mark_sync(f):
    return f  # no-op decorator



@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = None
    policy = asyncio.get_event_loop_policy()
    try:
        loop = policy.new_event_loop()
        policy.set_event_loop(loop)
        yield loop
    finally:
        if loop != None:
            loop.close()


@pytest_asyncio.fixture(scope="session")
async def init_db(event_loop):

    # create test database and init beanie
    client = AsyncIOMotorClient(settings.mongo_uri)
    db: AsyncIOMotorDatabase = getattr(client, settings.db_name)

    await init_beanie(db, document_models=[Account])
    yield db

    # destroy test database
    await client.drop_database(settings.db_name)
    client.close()


@pytest_asyncio.fixture(scope="session")
async def config_app(init_db):
    # configure petisco application to start dependencies
    application.configure(testing=True)
    yield

    # clear application data
    application.clear()


@pytest_asyncio.fixture(scope="session")
async def create_test_app(config_app):
    # create sanic test app manager
    test_app = application.get_app()
    yield test_app

    # cancel all pending tasks
    test_app.shutdown_tasks()
    test_app.stop()


@pytest_asyncio.fixture(scope="session")
def client_app_manager(create_test_app):
    return TestManager(create_test_app)
