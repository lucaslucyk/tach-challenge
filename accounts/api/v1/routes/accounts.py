from typing import List
from uuid import UUID
from pydantic import TypeAdapter
from sanic import Blueprint, json as json_response
from sanic.exceptions import NotFound, BadRequest
from sanic.request import Request
from sanic_ext import validate, openapi
from accounts.schemas.accounts import (
    Account,
    AccountCreate,
    AccountUpdate,
    AccountList,
)
from accounts.schemas.query import PaginateParams
from accounts.crud.account import accounts as accounts_crud

# TODO: Add swagger docs and move to Account controllers


blueprint = Blueprint("accounts")


@blueprint.get("/")
@openapi.response(
    200,
    {
        "application/json": AccountList.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
    },
    "Current accounts",
)
@validate(query=PaginateParams)
async def get_accounts(
    request: Request,
    query: PaginateParams,
) -> List[Account]:
    """List accounts"""
    result = await accounts_crud.list(
        skip=query.offset,
        limit=query.limit,
        sort=query.sort,
    )
    accounts = result.unwrap_or_else([])
    account_list = AccountList(
        accounts=(Account(**acc.model_dump(mode="json")) for acc in accounts)
    )
    return json_response(account_list.model_dump())


@blueprint.get("/<account_id:uuid>")
@openapi.response(
    200,
    {
        "application/json": Account.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
    },
    "Account data",
)
async def get_account_by_id(request: Request, account_id: UUID) -> Account:
    """Get account by id"""
    account = await accounts_crud.get(id=account_id)
    if account.is_failure:
        raise NotFound(f"Account {account_id} not found")
    out = Account(**account.get_value().model_dump(mode="json"))
    return json_response(out.model_dump(mode="json"))


@blueprint.get("/alias/<account_alias:str>")
@openapi.response(
    200,
    {
        "application/json": Account.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
    },
    "Account data",
)
async def get_account_by_alias(
    request: Request,
    account_alias: str,
) -> Account:
    """Get account by alias"""

    account = await accounts_crud.get_by_alias(alias=account_alias)
    if account.is_failure:
        raise NotFound(f"Account {account_alias} not found")
    out = Account(**account.get_value().model_dump(mode="json"))
    return json_response(out.model_dump(mode="json"))


@blueprint.post("/")
@openapi.body(
    {
        "application/json": AccountCreate.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
    },
    description="Account data",
    required=True,
)
@openapi.response(
    201,
    {
        "application/json": Account.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
    },
    "Account created",
)
@validate(json=AccountCreate)
async def create_account(request: Request, body: AccountCreate) -> Account:
    """Create new account"""
    new_account = await accounts_crud.create(body)
    if new_account.is_failure:
        raise BadRequest(f"Error creating account. Validate your data.")
    return json_response(new_account.get_value().model_dump(), status=201)


@blueprint.patch("/<account_id:uuid>")
@openapi.body(
    {
        "application/json": AccountUpdate.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
    },
    description="Account data",
    required=True,
)
@openapi.response(
    200,
    {
        "application/json": Account.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
    },
    "Account updated",
)
@validate(json=AccountUpdate)
async def update_account(
    request: Request,
    account_id: UUID,
    body: AccountUpdate,
) -> Account:
    """Update account"""

    account = await accounts_crud.get(id=account_id)
    if account.is_failure:
        raise NotFound(f"Account {account_id} not found")

    updated = await accounts_crud.update(account_id, body)
    if account.is_failure:
        raise BadRequest(f"Error updating account. Check your data.")

    out = Account(**updated.get_value().model_dump(mode="json"))
    return json_response(out.model_dump(mode="json"))


@blueprint.delete("/<account_id:uuid>")
@openapi.response(
    200,
    {
        "application/json": Account.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
    },
    "Account deleted",
)
async def delete_account(request: Request, account_id: UUID) -> Account:
    deleted = await accounts_crud.delete(account_id)
    if deleted.is_failure:
        raise NotFound(f"Account {account_id} not found")

    out = Account(**deleted.get_value().model_dump(mode="json"))
    return json_response(out.model_dump(mode="json"))
