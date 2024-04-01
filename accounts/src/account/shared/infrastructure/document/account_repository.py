from typing import List, Optional, Tuple
from beanie import SortDirection
from meiga import BoolResult, Error, Failure, Result, Success, isSuccess
from meiga.decorators import meiga
from petisco import (
    AggregateAlreadyExistError,
    AggregateNotFoundError,
    # CrudRepository,
    Uuid,
    databases,
)
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)
# from pymongo.client_session import ClientSession
from accounts.src.account.shared.domain.account import Account
from accounts.src.account.shared.infrastructure.document.account import (
    DocumentAccount,
)


class DocumentAccountRepository(AsyncCrudRepository[Account]):

    def __init__(self):
        self.document = DocumentAccount
        # self.session: ClientSession = databases.get(
        #     ClientSession,
        #     alias="document-accounts"
        # )

    @meiga
    async def save(
        self,
        account: Account,
    ) -> Result[Account, AggregateAlreadyExistError]:

        document_account = await self.document.find_one(
            self.document.aggregate_id == account.aggregate_id,
            # session=self.session,
        )
        if document_account:
            return Failure(AggregateAlreadyExistError(account.aggregate_id))

        document_account = self.document.from_domain(account)
        # await document_account.save(session=self.session)
        await document_account.save()

        return Success(document_account.to_domain())

    @meiga
    async def retrieve(self, aggregate_id: Uuid) -> Result[Account, Error]:
        document_account = await self.document.find_one(
            self.document.aggregate_id == aggregate_id,
            # session=self.session,
        )

        if not document_account:
            return Failure(AggregateNotFoundError(aggregate_id))

        account = document_account.to_domain()
        return Success(account)

    async def update(self, account: Account) -> Result[Account, Error]:

        document_account = await self.document.find_one(
            self.document.aggregate_id == account.aggregate_id.value,
            # session=self.session,
        )

        if not document_account:
            return Failure(AggregateNotFoundError(account.aggregate_id))

        document_account = self.document.from_domain(account)
        # TODO: Update this to update isSuccess global variable
        # await document_account.save(session=self.session)
        await document_account.save()
        return Success(document_account.to_domain())

    async def remove(self, aggregate_id: Uuid) -> Result[Account, Error]:

        document_account = await self.document.find_one(
            self.document.aggregate_id == aggregate_id, 
            # session=self.session, 
        )

        if not document_account:
            return Failure(AggregateNotFoundError(aggregate_id))

        # await document_account.delete(session=self.session)
        await document_account.delete()
        return Success(document_account)

    async def retrieve_all(
        self,
        skip: int = 0,
        limit: int = 100,
        sort: Optional[List[Tuple[str, SortDirection]]] = None,
    ) -> Result[list[Account], Error]:

        documents = await self.document.all(
            skip=skip,
            limit=limit,
            sort=sort,
            # session=self.session,
        ).to_list(length=limit)
        return Success([doc.to_domain() for doc in documents])

    async def clear(self) -> None:

        # await self.document.delete_all(session=self.session)
        await self.document.delete_all()
