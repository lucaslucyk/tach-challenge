from sanic import Blueprint
from sanic.request import Request
from sanic.response import json as json_response
from sanic_ext import validate, openapi
from accounts.api.models import AccountIn, AccountOut, AccountList, Paginator
from accounts.src.account.create.application.create_account_controller import (
    CreateAccountController,
)
from accounts.src.account.retrieve_all.application.retrieve_all_accounts_controller import (
    RetrieveAllAccountsController,
)

blueprint = Blueprint("accounts", version=1)


@blueprint.post("/")
@openapi.body(
    {
        "application/json": AccountIn.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
    },
    description="Account data",
    required=True,
)
@validate(json=AccountIn)
async def create_account(request: Request, body: AccountIn):
    result = await CreateAccountController().execute(body.to_account())
    if result.is_failure:
        result.transform()
    return json_response(
        AccountOut.from_account(result.value).model_dump(mode="json")
    )


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
@openapi.parameter("limit", "number", "query")
@validate(query=Paginator)
async def retrieve_all_accounts(request: Request, query: Paginator):
    # TODO: add all parameters from model and add to controller
    result = await RetrieveAllAccountsController().execute()
    return json_response(
        AccountList.from_accounts(result.value).model_dump(mode="json")
    )
