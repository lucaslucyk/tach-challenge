from unittest.mock import Mock

import pytest
from meiga import isFailure
from meiga.assertions import assert_failure, assert_success
from petisco import DomainEventBus
from accounts.src.account.create.application.account_creator import (
    AccountCreator,
)
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)
from tests.accounts.mothers.account_mother import AccountMother
from tests.conftest import pytest_mark_asyncio


# @pytest.mark.unit
@pytest_mark_asyncio
class TestAccountCreator:
    mock_repository: Mock
    mock_domain_event_bus: Mock

    def setup_method(self):
        self.mock_repository = Mock(AsyncCrudRepository)
        self.mock_domain_event_bus = Mock(DomainEventBus)

    async def should_success_when_happy_path(self):
        account_creator = AccountCreator(
            repository=self.mock_repository,
            domain_event_bus=self.mock_domain_event_bus,
        )

        result = await account_creator.execute(AccountMother.any())
        assert_success(result)

        self.mock_repository.save.assert_called_once()
        # self.mock_domain_event_bus.publish.assert_called_once()


    async def should_failure_when_repository_fails(self):
        self.mock_repository.save = Mock(return_value=isFailure)

        account_creator = AccountCreator(
            repository=self.mock_repository,
            domain_event_bus=self.mock_domain_event_bus,
        )

        result = await account_creator.execute(AccountMother.any())
        assert_failure(result)

        self.mock_repository.save.assert_called_once()
        self.mock_domain_event_bus.publish.assert_not_called()
