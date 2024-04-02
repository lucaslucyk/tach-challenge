from typing import Literal
from uuid import UUID
from meiga import (
    AnyResult,
    Error,
    Failure,
    Result,
    Success,
)
from meiga.decorators import meiga
from petisco import AggregateNotFoundError, AsyncUseCase, DomainEventBus

from accounts.src.account.shared.domain.events import (
    AccountNotAvailable,
    AccountNotFound,
    FundsMoved,
    IncompleteTransaction,
    InsufficientFunds,
    SymbolError,
)
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)
from petisco.base.domain.errors.defaults.not_found import NotFound
from accounts.src.account.shared.domain.account import Account
from accounts.src.transaction.shared.domain.transaction import Transaction


class FundsMover(AsyncUseCase):

    def __init__(
        self,
        repository: AsyncCrudRepository,
        domain_event_bus: DomainEventBus,
    ):
        self.repository = repository
        self.domain_event_bus = domain_event_bus

    async def account_or_error(
        self,
        transaction: Transaction,
        attr: Literal["source_account_id", "target_account_id"],
    ) -> Result[Account, Error]:
        """Get account from repository and publish event and raise if not found.

        Args:
            transaction (Transaction): Inner transaction
            attr Literal["source_account_id", "target_account_id"]: account kind

        Returns:
            Result[Account, Error]: Domain Account or error
        """

        account_id: UUID = getattr(transaction, attr, None)
        if not account_id:
            return Failure(Error("Must specify the transaction kind"))

        account = await self.repository.retrieve(account_id)
        if account.is_failure:
            transaction.record(
                AccountNotFound(
                    account_id=str(account_id),
                    trigger=transaction.model_dump(mode="json"),
                )
            )
            self.domain_event_bus.publish(transaction.pull_domain_events())
            return Failure(NotFound(f"Account {account_id} not found"))
        return account

    async def execute(self, transaction: Transaction) -> AnyResult:
        source = await self.account_or_error(transaction, "source_account_id")
        source = source.unwrap_or_raise()

        target = await self.account_or_error(transaction, "target_account_id")
        target = target.unwrap_or_raise()

        # check active accounts
        if not source.active:
            transaction.record(
                AccountNotAvailable(
                    trigger=transaction.model_dump(mode="json"),
                    account_id=str(source.aggregate_id),
                )
            )
            self.domain_event_bus.publish(transaction.pull_domain_events())
            return Failure(
                Error(f"Account {source.aggregate_id} not available")
            )

        # check active accounts
        if not target.active:
            transaction.record(
                AccountNotAvailable(
                    trigger=transaction.model_dump(mode="json"),
                    account_id=str(target.aggregate_id),
                )
            )
            self.domain_event_bus.publish(transaction.pull_domain_events())
            return Failure(
                Error(f"Account {target.aggregate_id} not available")
            )

        # check symbols
        if (
            source.symbol != target.symbol
            or source.symbol != transaction.symbol
        ):
            transaction.record(
                SymbolError(
                    trigger=transaction.model_dump(mode="json"),
                    source_symbol=source.symbol,
                    target_symbol=target.symbol,
                )
            )
            self.domain_event_bus.publish(transaction.pull_domain_events())
            return Failure(Error(f"Symbols do not match"))

        # check balance
        if source.balance - transaction.amount < 0.0:
            transaction.record(
                InsufficientFunds(
                    trigger=transaction.model_dump(mode="json"),
                    account_id=str(source.aggregate_id),
                )
            )
            self.domain_event_bus.publish(transaction.pull_domain_events())
            return Failure(
                Error(
                    f"Account {source.aggregate_id} does not have sufficient funds"
                )
            )

        # deduct funds from source account
        source.balance -= transaction.amount
        source = await self.repository.update(source)
        if source.is_failure:
            transaction.record(
                IncompleteTransaction(
                    trigger=transaction.model_dump(mode="json"),
                )
            )
            self.domain_event_bus.publish(transaction.pull_domain_events())
            return Failure(
                Error("Funds could not be deducted from the source account")
            )

        # add funds to target account
        target.balance += transaction.amount
        target = await self.repository.update(target)
        if target.is_failure:
            transaction.record(
                IncompleteTransaction(
                    trigger=transaction.model_dump(mode="json"),
                )
            )
            self.domain_event_bus.publish(transaction.pull_domain_events())
            return Failure(
                Error("Funds could not be deducted from the target account")
            )

        # transaction completed successfully
        transaction.record(
            FundsMoved(
                trigger=transaction.model_dump(mode="json"),
            )
        )
        self.domain_event_bus.publish(transaction.pull_domain_events())
        return Success("Transaction completed")
