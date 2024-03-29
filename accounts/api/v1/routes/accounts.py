from typing import List
from uuid import UUID
from sanic import Blueprint, json as json_response
from sanic.exceptions import NotFound
from sanic.request import Request
from sanic_ext import validate, openapi
from accounts.schemas.accounts import Account, AccountCreate, AccountUpdate
from accounts.schemas.query import PaginateParams
from accounts.crud.account import accounts as accounts_crud

# TODO: Add swagger docs and move to Account controllers


blueprint = Blueprint("accounts")


@blueprint.get("/")
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
    out_acc = [Account(**acc.model_dump(mode="json")) for acc in accounts]
    return json_response([out.model_dump(mode="json") for out in out_acc])


@blueprint.get("/<account_id:uuid>")
async def get_account_by_id(request: Request, account_id: UUID) -> Account:
    """Get account by id"""
    account = await accounts_crud.get(id=account_id)
    if account.is_failure:
        raise NotFound(f"Account {account_id} not found")
    out = Account(**account.get_value().model_dump(mode="json"))
    return json_response(out.model_dump(mode="json"))


@blueprint.get("/alias/<account_alias:str>")
async def get_account_by_alias(
    request: Request,
    account_alias: str,
) -> Account:
    """Get account by id"""

    account = await accounts_crud.get_by_alias(alias=account_alias)
    if account.is_failure:
        raise NotFound(f"Account {account_alias} not found")
    out = Account(**account.get_value().model_dump(mode="json"))
    return json_response(out.model_dump(mode="json"))


@blueprint.post("/")
# @openapi.body(
#     {"application/json": AccountCreate.model_json_schema()},
#     description="Body description",
#     required=True,
#     validate=True,
# )
@openapi.definition(
    body={
        "application/json": AccountCreate.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
    },
)
@validate(json=AccountCreate)
async def create_account(request: Request, body: AccountCreate) -> Account:
    """Create new account"""
    new_account = await accounts_crud.create(body)
    new_account = new_account.unwrap_or_raise()
    return json_response(new_account.model_dump())


@blueprint.patch("/<account_id:uuid>")
@openapi.definition(
    body={
        "application/json": AccountUpdate.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
    },
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
        raise NotFound(f"Account {account_id} not found")

    out = Account(**updated.get_value().model_dump(mode="json"))

    return json_response(out.model_dump(mode="json"))


@blueprint.delete("/<account_id:uuid>")
async def delete_account(request: Request, account_id: UUID) -> Account:
    deleted = await accounts_crud.delete(account_id)
    if deleted.is_failure:
        raise NotFound(f"Account {account_id} not found")

    out = Account(**deleted.get_value().model_dump(mode="json"))
    return json_response(out.model_dump(mode="json"))
