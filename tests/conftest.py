import pytest
from sanic_testing.manager import TestManager
from accounts.application import application


application.configure(testing=True)
test_app = application.get_app()


@pytest.fixture
def client_app_manager():
    return TestManager(test_app)
