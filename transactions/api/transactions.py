from uuid import UUID
from petisco import Uuid
from sanic import Blueprint
from sanic.request import Request
from sanic.response import json as json_response
from sanic_ext import validate, openapi
from transactions.api.models import (
    TransactionIn,
    TransactionOut,
    TransactionList,
    Paginator,
)
from transactions.src.transaction.create.application.create_transaction_controller import (
    CreateTransactionController,
)
from transactions.src.transaction.delete.application.delete_transaction_controller import (
    DeleteTransactionController,
)
from transactions.src.transaction.retrieve.application.retrieve_transaction_controller import (
    RetrieveTransactionController,
)
from transactions.src.transaction.retrieve_all.application.retrieve_all_transactions_controller import (
    RetrieveAllTransactionsController,
)
from transactions.src.transaction.update.application.update_transaction_controller import (
    UpdateTransactionController,
)

blueprint = Blueprint("transactions", version=1)


@blueprint.post("/")
@openapi.body(
    {
        "application/json": TransactionIn.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
    },
    description="Transaction data",
    required=True,
)
@openapi.response(
    201,
    {
        "application/json": TransactionOut.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
    },
    "Transaction data",
)
@validate(json=TransactionIn)
async def create_transaction(request: Request, body: TransactionIn):
    result = await CreateTransactionController().execute(body.to_transaction())
    if result.is_failure:
        result.transform()
    return json_response(
        body=TransactionOut.from_transaction(result.value).model_dump(
            mode="json"
        ),
        status=201,
    )


@blueprint.get("/")
@openapi.response(
    200,
    {
        "application/json": TransactionList.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
    },
    "Current transactions",
)
@openapi.parameter("limit", int, "query")
@openapi.parameter("skip", int, "query")
@validate(query=Paginator)
async def retrieve_all_transactions(request: Request, query: Paginator):
    result = await RetrieveAllTransactionsController().execute(
        **query.model_dump(mode="json", exclude_unset=True)
    )
    return json_response(
        TransactionList.from_transactions(result.value).model_dump(mode="json")
    )


@blueprint.get("/<id:uuid>")
@openapi.response(
    200,
    {
        "application/json": TransactionOut.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
    },
    "Transaction data",
)
async def get_transaction_by_id(request: Request, id: UUID):
    """Get transaction by id"""

    aggregate_id = Uuid(str(id))
    result = await RetrieveTransactionController().execute(aggregate_id)
    if result.is_failure:
        result.transform()
    return json_response(
        TransactionOut.from_transaction(result.value).model_dump(mode="json")
    )


@blueprint.delete("/<id:uuid>")
@openapi.response(
    200,
    {
        "application/json": TransactionOut.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
    },
    "Transaction deleted",
)
async def delete_transaction(request: Request, id: UUID):
    aggregate_id = Uuid(str(id))
    result = await DeleteTransactionController().execute(aggregate_id)
    if result.is_failure:
        result.transform()
    return json_response(
        TransactionOut.from_transaction(result.value).model_dump(mode="json")
    )


@blueprint.patch("/")
@openapi.body(
    {
        "application/json": TransactionIn.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
    },
    description="Transaction data",
    required=True,
)
@openapi.response(
    200,
    {
        "application/json": TransactionOut.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
    },
    "Transaction data",
)
@validate(json=TransactionIn)
async def update_transaction(request: Request, body: TransactionIn):
    result = await UpdateTransactionController().execute(body.to_transaction())
    if result.is_failure:
        result.transform()
    return json_response(
        TransactionOut.from_transaction(result.value).model_dump(mode="json")
    )
