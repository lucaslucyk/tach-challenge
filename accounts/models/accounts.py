from typing import Annotated, Optional
from beanie import Indexed
from pydantic import Field
from uuid import UUID, uuid4
from beanie_crud.models import ModelBase


class Account(ModelBase):
    id: UUID = Field(default_factory=uuid4)
    alias: Annotated[str, Indexed(str, unique=True)]
    name: str
    active: bool
    balance: float
    symbol: str

    def __repr__(self):
        return (
            "{}(alias={}, name={}, active={}, symbol={}, balance={})",
            format(
                self.__class__.__name__,
                self.alias,
                self.name,
                self.active,
                self.balance,
                self.symbol,
            ),
        )

    def __str__(self):
        return self.alias

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other: "Account") -> bool:
        if isinstance(other, Account):
            return self.id == other.id
        return False

    @classmethod
    async def by_alias(cls, alias: str) -> Optional["Account"]:
        return await cls.find_one(cls.alias == alias)
