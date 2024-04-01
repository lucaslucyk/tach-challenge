from typing import List, Optional, Tuple
from beanie import SortDirection
from beanie.odm.operators.find.comparison import Eq
from meiga import BoolResult, Error, Failure, Result, Success, isSuccess
from meiga.decorators import meiga
from petisco import (
    AggregateAlreadyExistError,
    AggregateNotFoundError,
    # CrudRepository,
    Uuid,
    databases,
)
from petisco.base.domain.errors.defaults.already_exists import AlreadyExists
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
    ) -> Result[Account, AggregateAlreadyExistError | AlreadyExists]:

        # check if exists an account with received id
        if await self.document.find_one(
            self.document.aggregate_id == account.aggregate_id.value
        ).exists():
            return Failure(
                AggregateAlreadyExistError(account.aggregate_id.value)
            )

        # check if exists an account with received alias
        if await self.document.find_one(
            self.document.alias == account.alias
        ).exists():
            return Failure(
                AlreadyExists(additional_info={"alias": account.alias})
            )

        # conditions = [
        #     Eq(self.document.aggregate_id, account.aggregate_id.value),
        #     Eq(self.document.alias, account.alias),
        # ]
        # document_account = await self.document.find_one({"$or": conditions})
        # if document_account:
        #     return Failure(
        #         AlreadyExists(
        #             account_id=(
        #                 str(account.aggregate_id.value)
        #                 if account.aggregate_id
        #                 else None
        #             ),
        #             additional_info=account.alias,
        #         ),
        #     )

        document_account = self.document.from_domain(account)
        
        # await document_account.save(session=self.session)
        document_account = await document_account.save()

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
