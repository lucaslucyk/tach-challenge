from abc import abstractmethod
from typing import Generic, List, TypeVar

from meiga import Error, NotImplementedMethodError, Result

from petisco.base.application.patterns.repository import Repository
from petisco.base.domain.model.aggregate_root import AggregateRoot
from petisco.base.domain.model.uuid import Uuid

AggregateRootType = TypeVar("AggregateRootType", bound=AggregateRoot)


class AsyncCrudRepository(Generic[AggregateRootType], Repository):
    @abstractmethod
    async def save(
        self, aggregate_root: AggregateRootType
    ) -> Result[AggregateRootType, Error]:
        return NotImplementedMethodError

    @abstractmethod
    async def retrieve(
        self, aggregate_id: Uuid
    ) -> Result[AggregateRootType, Error]:
        return NotImplementedMethodError

    @abstractmethod
    async def update(
        self, aggregate_root: AggregateRootType
    ) -> Result[AggregateRootType, Error]:
        return NotImplementedMethodError

    @abstractmethod
    async def remove(
        self, aggregate_id: Uuid
    ) -> Result[AggregateRootType, Error]:
        return NotImplementedMethodError

    @abstractmethod
    async def retrieve_all(self) -> Result[List[AggregateRootType], Error]:
        return NotImplementedMethodError
