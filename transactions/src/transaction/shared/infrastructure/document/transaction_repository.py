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
from transactions.src.transaction.shared.domain.transaction import Transaction
from transactions.src.transaction.shared.infrastructure.document.transaction import (
    DocumentTransaction,
)


class DocumentTransactionRepository(AsyncCrudRepository[Transaction]):

    def __init__(self):
        self.document = DocumentTransaction

    @meiga
    async def save(
        self,
        transaction: Transaction,
    ) -> Result[Transaction, Union[AggregateAlreadyExistError, AlreadyExists]]:
        """Create a document transaction from inner domain transaction

        Args:
            transaction (Transaction): Domain transaction

        Returns:
            Result[Transaction, Union[AggregateAlreadyExistError, AlreadyExists]]:
                Success result with Domain transaction if created successfully.
                Failure result with AggregateAlreadyExistError if exists an
                transaction with received id.
                Failure result with AlreadyExists if exists an transaction with
                received alias.
        """

        # check if exists an transaction with received id
        if await self.document.find_one(
            Eq(self.document.aggregate_id, transaction.aggregate_id.value)
        ).exists():
            return Failure(
                AggregateAlreadyExistError(transaction.aggregate_id.value)
            )

        # save document
        document_transaction = self.document.from_domain(transaction)
        document_transaction = await document_transaction.save()

        # cast to domain format
        return Success(document_transaction.to_domain())

    @meiga
    async def retrieve(self, aggregate_id: Uuid) -> Result[Transaction, Error]:
        """Retreive an transaction by aggregate id

        Args:
            aggregate_id (Uuid): Aggregate id

        Returns:
            Result[Transaction, Error]: Domain Transaction or error
        """
        
        if not isinstance(aggregate_id, Uuid):
            aggregate_id = Uuid(aggregate_id)
        document_transaction = await self.document.find_one(
            self.document.aggregate_id == aggregate_id.value,
        )

        if not document_transaction:
            return Failure(AggregateNotFoundError(aggregate_id))

        # cast to domain format
        transaction = document_transaction.to_domain()
        return Success(transaction)

    @meiga
    async def update(self, transaction: Transaction) -> Result[Transaction, Error]:
        document_transaction = await self.document.find_one(
            self.document.aggregate_id == transaction.aggregate_id.value,
        )

        if not document_transaction:
            return Failure(AggregateNotFoundError(transaction.aggregate_id))
        
        # TODO: check if transaction is locked (pending) before update

        document = self.document.from_domain(transaction)
        # ensure keep original data
        document.id = document_transaction.id
        document.created_at = document_transaction.created_at
        
        document = await document.save()
        return Success(document.to_domain())

    @meiga
    async def remove(self, aggregate_id: Uuid) -> Result[Transaction, Error]:
        if not isinstance(aggregate_id, Uuid):
            aggregate_id = Uuid(aggregate_id)

        document_transaction = await self.document.find_one(
            self.document.aggregate_id == aggregate_id.value
        )

        if not document_transaction:
            return Failure(AggregateNotFoundError(aggregate_id))

        # TODO: Check if transaction is locked (pending) before delete
        _ = await document_transaction.delete()
        return Success(document_transaction.to_domain())

    @meiga
    async def retrieve_all(
        self,
        skip: int = 0,
        limit: int = 100,
        sort: Optional[List[Tuple[str, SortDirection]]] = None,
    ) -> Result[list[Transaction], Error]:

        documents = await self.document.all(
            skip=skip,
            limit=limit,
            sort=sort,
        ).to_list(length=limit)
        return Success([doc.to_domain() for doc in documents])

    async def clear(self) -> None:
        await self.document.delete_all()
