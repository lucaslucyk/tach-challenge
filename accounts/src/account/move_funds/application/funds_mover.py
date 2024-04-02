from typing import Literal
from uuid import UUID
from meiga import (
    AnyResult,
    BoolResult,
    Error,
    Failure,
    Result,
    Success,
)
from meiga.decorators import meiga
from petisco import AsyncUseCase, DomainEventBus

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

    def check_active(
        self, account: Account, transaction: Transaction
    ) -> BoolResult:
        # check active accounts
        if not account.active:
            transaction.record(
                AccountNotAvailable(
                    trigger=transaction.model_dump(mode="json"),
                    account_id=str(account.aggregate_id),
                )
            )
            self.domain_event_bus.publish(transaction.pull_domain_events())
            return Failure(
                Error(f"Account {account.aggregate_id} not available")
            )
        return Success()

    def check_symbols(
        self, transaction: Transaction, source: Account, target: Account
    ) -> BoolResult:
        _checks = (
            source.symbol != target.symbol,
            source.symbol != transaction.symbol,
        )
        if any(_checks):
            transaction.record(
                SymbolError(
                    trigger=transaction.model_dump(mode="json"),
                    source_symbol=source.symbol,
                    target_symbol=target.symbol,
                )
            )
            self.domain_event_bus.publish(transaction.pull_domain_events())
            return Failure(Error(f"Symbols do not match"))

        return Success()

    def check_funds(
        self, account: Account, transaction: Transaction
    ) -> BoolResult:
        # check balance
        if account.balance - transaction.amount < 0.0:
            transaction.record(
                InsufficientFunds(
                    trigger=transaction.model_dump(mode="json"),
                    account_id=str(account.aggregate_id),
                )
            )
            self.domain_event_bus.publish(transaction.pull_domain_events())
            return Failure(
                Error(
                    f"Account {account.aggregate_id} does not have sufficient funds"
                )
            )
        return Success()

    async def move_funds(
        self,
        account: Account,
        action: Literal["add", "sub"],
        transaction: Transaction,
    ) -> AnyResult:
        # apply changes to account balance
        match action:
            case "add":
                account.balance += transaction.amount
            case "sub":
                account.balance -= transaction.amount
            case _:
                return Failure(Error("Invalid action"))

        # update account
        result = await self.repository.update(account)
        if result.is_failure:
            transaction.record(
                IncompleteTransaction(
                    trigger=transaction.model_dump(mode="json"),
                )
            )
            self.domain_event_bus.publish(transaction.pull_domain_events())
            return Failure(
                Error("Funds could not be deducted from the account account")
            )

        return Success()

    @meiga
    async def execute(self, transaction: Transaction) -> AnyResult:
        # get source account
        source = (
            await self.account_or_error(transaction, "source_account_id")
        ).unwrap_or_raise()

        # get target account
        target = (
            await self.account_or_error(transaction, "target_account_id")
        ).unwrap_or_raise()

        # check actives
        _ = self.check_active(source, transaction).unwrap_or_raise()
        _ = self.check_active(target, transaction).unwrap_or_raise()

        # check symbols
        _ = self.check_symbols(transaction, source, target).unwrap_or_raise()

        # check balance
        _ = self.check_funds(source, transaction).unwrap_or_raise()

        # deduct funds from source account
        _ = (
            await self.move_funds(source, "sub", transaction)
        ).unwrap_or_raise()
        _ = (
            await self.move_funds(target, "add", transaction)
        ).unwrap_or_raise()

        # transaction completed successfully
        transaction.record(
            FundsMoved(
                trigger=transaction.model_dump(mode="json"),
            )
        )
        self.domain_event_bus.publish(transaction.pull_domain_events())
        return Success("Transaction completed")
