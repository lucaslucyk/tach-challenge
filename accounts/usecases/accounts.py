from dataclasses import dataclass
from uuid import UUID
from meiga import Error, Failure, Result, Success
from petisco import AsyncUseCase
from accounts.repositories.accounts import AccountsRepository
from accounts.schemas.accounts import (
    AccountCreate,
    AccountList,
    Account,
    AccountUpdate,
)
from accounts.schemas.query import PaginateParams
from accounts.usecases.errors import FundsError, SymbolError
from beanie_crud.errors import NotFound


@dataclass
class AccountBase:
    accounts_repository: AccountsRepository = AccountsRepository()


class GetAccounts(AsyncUseCase, AccountBase):

    async def execute(
        self,
        params: PaginateParams,
        **kwargs,
    ) -> Result[AccountList, Error]:
        result = await self.accounts_repository.list(
            skip=params.offset,
            limit=params.limit,
            sort=params.sort,
            **kwargs,
        )
        accounts = result.unwrap_or_return()
        account_list = AccountList(
            accounts=(
                Account(**acc.model_dump(mode="json")) for acc in accounts
            )
        )
        return Success(account_list)


class GetAccountById(AsyncUseCase, AccountBase):
    async def execute(self, account_id: UUID) -> Result[Account, NotFound]:
        result = await self.accounts_repository.get(account_id)
        account = result.unwrap_or_return()
        return Success(Account(**account.model_dump(mode="json")))


class GetAccountByAlias(AsyncUseCase, AccountBase):
    async def execute(self, alias: str) -> Result[Account, Error]:
        result = await self.accounts_repository.get_by_alias(alias)
        account = result.unwrap_or_return()
        return Success(Account(**account.model_dump(mode="json")))


class CreateAccount(AsyncUseCase, AccountBase):
    async def execute(self, account: AccountCreate) -> Result[Account, Error]:
        result = await self.accounts_repository.create(account)
        account = result.unwrap_or_return()
        return Success(Account(**account.model_dump(mode="json")))


class UpdateAccount(AsyncUseCase, AccountBase):
    async def execute(
        self,
        account_id: UUID,
        account: AccountUpdate,
    ) -> Result[Account, Error]:
        result = await self.accounts_repository.update(account_id, account)
        account = result.unwrap_or_return()
        return Success(Account(**account.model_dump(mode="json")))


class DeleteAccount(AsyncUseCase, AccountBase):
    async def execute(self, account_id: UUID) -> Result[Account, Error]:
        result = await self.accounts_repository.delete(account_id)
        account = result.unwrap_or_return()
        return Success(Account(**account.model_dump(mode="json")))


class GetBalance(AsyncUseCase, AccountBase):
    async def execute(self, account_id: UUID) -> Result[int, Error]:
        result = await self.accounts_repository.get(account_id)
        account = result.unwrap_or_return()
        return Success(account.balance)


class AddAccountFunds(AsyncUseCase, AccountBase):
    async def execute(
        self,
        account_id: UUID,
        ammount: float,
        symbol: str,
    ) -> Result[Account, SymbolError]:

        acc = await self.accounts_repository.get(account_id)
        acc = acc.unwrap_or_return()
        if acc.symbol != symbol:
            return Failure(SymbolError(f"The Account symbol is {acc.symbol}"))

        acc.balance += ammount
        acc = await acc.save()

        return Success(Account(**acc.model_dump(mode="json")))


class SubstractAccountFunds(AsyncUseCase, AccountBase):
    async def execute(
        self,
        account_id: UUID,
        ammount: float,
        symbol: str,
    ) -> Result[Account, SymbolError]:

        acc = await self.accounts_repository.get(account_id)
        acc = acc.unwrap_or_return()
        if acc.symbol != symbol:
            return Failure(SymbolError(f"The Account symbol is <{acc.symbol}>"))

        if acc.balance - ammount < 0.0:
            return Failure(FundsError(f"Insufficient Funds"))

        acc.balance -= ammount
        acc = await acc.save()

        return Success(Account(**acc.model_dump(mode="json")))
