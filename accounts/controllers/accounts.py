from typing import Any
from uuid import UUID
from meiga import AnyResult, Error, Failure, Result, Success
from petisco import AsyncController
from sanic import BadRequest, NotFound as NotFoundResponse, json
from accounts.schemas.accounts import AccountList, Account
from accounts.schemas.query import PaginateParams
from accounts.usecases.accounts import (
    GetAccounts as GetAccountsUseCase,
    GetAccountById as AccountByIdUseCase
)
from beanie_crud.errors import NotFound
from sanic.response import JSONResponse


class AccountsController(AsyncController):

    class Config:
        error_map = {
            Error: (404, "Account error"),
        }

    async def execute(
        self,
        params: PaginateParams,
        **kwargs,
    ) -> Result[AccountList, Any]:
        
        return await GetAccountsUseCase().execute(params, **kwargs)


class AccountByIdController(AsyncController):

    async def execute(self, account_id: UUID) -> Result[Account, NotFound]:
        return await AccountByIdUseCase().execute(account_id)