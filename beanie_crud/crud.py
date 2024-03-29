from abc import ABC, abstractproperty
from typing import (
    Any,
    Generic,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
)
from uuid import UUID
from meiga import Error, Failure, Result, Success
from beanie import SortDirection
from beanie_crud.errors import NotFound
from beanie_crud.models import CreateSchemaType, DocumentType, UpdateSchemaType


class CRUDBase(Generic[DocumentType, CreateSchemaType, UpdateSchemaType], ABC):
    @abstractproperty
    def document(self) -> Type[DocumentType]: ...

    async def get(self, id: UUID, **kwargs) -> Result[DocumentType, NotFound]:
        # await self.document.get(id)
        document = await self.document.get(id, **kwargs)
        if not document:
            return Failure(NotFound())
        return Success(document)

    async def list(
        self,
        skip: int = 0,
        limit: int = 100,
        sort: Optional[List[Tuple[str, SortDirection]]] = None,
        **kwargs
    ) -> Result[List[DocumentType], Error]:
        # TODO: add validation and parse errors
        documents = await self.document.all(
            skip=skip, limit=limit, sort=sort, **kwargs
        ).to_list(length=limit)
        return Success(documents)

    async def find_one(
        self, *clauses: Mapping[str, Any] | bool, **kwargs
    ) -> Result[DocumentType, NotFound]:
        document = await self.document.find_one(*clauses, **kwargs)
        if not document:
            return Failure(NotFound())
        return Success(document)

    async def filter(
        self, *clauses: Mapping[str, Any] | bool, **kwargs
    ) -> Result[Iterable[DocumentType], Error]:
        # TODO: add validation and parse errors
        document = await self.document.find(*clauses, **kwargs)
        return Success(document)

    async def create(
        self,
        data: CreateSchemaType,
    ) -> Result[DocumentType, Error]:
        # TODO: add validation and parse errors
        document = await self.document(
            **data.model_dump(exclude_unset=True)
        ).save()
        return Success(document)

    async def bulk_create(
        self,
        data: Sequence[CreateSchemaType],
    ) -> Result[Sequence[DocumentType], Error]:
        # TODO: add validation and parse errors
        documents = await self.document.insert(data)
        return Success(documents)

    async def update(
        self,
        id: UUID,
        data: UpdateSchemaType,
    ) -> Result[DocumentType, NotFound]:
        # TODO: add validation and parse errors
        obj = await self.get(id=id)
        obj = obj.unwrap_or_return(obj)
        document = obj.get_value()
        document = document.model_copy(
            update=data.model_dump(exclude_unset=True)
        )
        return Success(await document.save())

    async def delete(self, id: UUID) -> Result[DocumentType, NotFound]:
        # TODO: add validation and parse errors
        obj = await self.get(id=id)
        obj = obj.unwrap_or_return(obj)
        return Success(await obj.get_value().delete())
