from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from beanie import Indexed
from petisco import Uuid
from pydantic import Field
import pymongo
from petisco_sanic.extra.beanie.document.document_base import DocumentBase
from accounts.src.account.shared.domain.account import Account


class DocumentAccount(DocumentBase[Account]):

    # __tablename__ = "Account"

    # beanie
    id: UUID = Field(default_factory=uuid4)
    aggregate_id: Annotated[str, Indexed(str, unique=True)]
    alias: Annotated[str, Indexed(str, unique=True)]
    name: str = Field(..., min_length=5, max_length=100)
    symbol: str
    balance: float = Field(..., ge=0.0)
    active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "accounts"
        indexes = [
            [
                ("alias", pymongo.TEXT),
                ("aggregate_id", pymongo.TEXT),
            ],
        ]

    def to_domain(self) -> Account:
        return Account(
            alias=self.alias,
            name=self.name,
            symbol=self.symbol,
            balance=self.balance,
            active=self.active,
            aggregate_id=Uuid(self.aggregate_id),
            created_at=self.created_at,
        )

    @staticmethod
    def from_domain(account: Account) -> "DocumentAccount":
        return DocumentAccount(
            alias=account.alias,
            name=account.name,
            symbol=account.symbol,
            balance=account.balance,
            active=account.active,
            aggregate_id=Uuid(account.aggregate_id),
            created_at=account.created_at,
        )
