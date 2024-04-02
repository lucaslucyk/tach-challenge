from typing import List, Optional, Tuple, Union
from beanie import SortDirection
from beanie.odm.operators.find.comparison import Eq
from meiga import Error, Failure, Result, Success
from meiga.decorators import meiga
from petisco import (
    AggregateAlreadyExistError,
    AggregateNotFoundError,
    Uuid,
)
from petisco.base.domain.errors.defaults.already_exists import AlreadyExists
from petisco_sanic.base.application.patterns.async_crud_repository import (
    AsyncCrudRepository,
)
from accounts.src.account.shared.domain.account import Account
from accounts.src.account.shared.infrastructure.document.account import (
    DocumentAccount,
)


class DocumentAccountRepository(AsyncCrudRepository[Account]):

    def __init__(self):
        self.document = DocumentAccount

    @meiga
    async def save(
        self,
        account: Account,
    ) -> Result[Account, Union[AggregateAlreadyExistError, AlreadyExists]]:
        """Create a document account from inner domain account

        Args:
            account (Account): Domain account

        Returns:
            Result[Account, Union[AggregateAlreadyExistError, AlreadyExists]]:
                Success result with Domain account if created successfully.
                Failure result with AggregateAlreadyExistError if exists an
                account with received id.
                Failure result with AlreadyExists if exists an account with
                received alias.
        """

        # check if exists an account with received id
        if await self.document.find_one(
            Eq(self.document.aggregate_id, account.aggregate_id.value)
        ).exists():
            return Failure(
                AggregateAlreadyExistError(account.aggregate_id.value)
            )

        # check if exists an account with received alias
        if await self.document.find_one(
            Eq(self.document.alias, account.alias)
        ).exists():
            return Failure(
                AlreadyExists(additional_info={"alias": account.alias})
            )

        # save document
        document_account = self.document.from_domain(account)
        document_account = await document_account.save()

        # cast to domain format
        return Success(document_account.to_domain())

    @meiga
    async def retrieve(self, aggregate_id: Uuid) -> Result[Account, Error]:
        """Retreive an account by aggregate id

        Args:
            aggregate_id (Uuid): Aggregate id

        Returns:
            Result[Account, Error]: Domain Account or error
        """
        
        if not isinstance(aggregate_id, Uuid):
            aggregate_id = Uuid(aggregate_id)
        try:
            document_account = await self.document.find_one(
                self.document.aggregate_id == aggregate_id.value,
            )
        except Exception as err:
            return Failure(err)

        if not document_account:
            return Failure(AggregateNotFoundError(aggregate_id))

        # cast to domain format
        account = document_account.to_domain()
        return Success(account)

    @meiga
    async def update(self, account: Account) -> Result[Account, Error]:
        document_account = await self.document.find_one(
            self.document.aggregate_id == account.aggregate_id.value,
        )

        if not document_account:
            return Failure(AggregateNotFoundError(account.aggregate_id))
                
        document = self.document.from_domain(account)
        document.id = document_account.id
        document = await document.save()
        return Success(document.to_domain())

    @meiga
    async def remove(self, aggregate_id: Uuid) -> Result[Account, Error]:
        if not isinstance(aggregate_id, Uuid):
            aggregate_id = Uuid(aggregate_id)

        document_account = await self.document.find_one(
            self.document.aggregate_id == aggregate_id,
        )

        if not document_account:
            return Failure(AggregateNotFoundError(aggregate_id))

        document_account = await document_account.delete()
        return Success(document_account.to_domain())

    @meiga
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
        ).to_list(length=limit)
        return Success([doc.to_domain() for doc in documents])

    async def clear(self) -> None:
        await self.document.delete_all()
