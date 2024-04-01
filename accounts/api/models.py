from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from sanic_ext import openapi
from accounts.src.account.shared.domain.account import Account


class Base(BaseModel):
    class Config:
        extra = "ignore"


@openapi.component
class AccountIn(Base):
    alias: str = Field(..., min_length=8, max_length=50)
    name: str = Field(..., min_length=5, max_length=100)
    symbol: str
    balance: float = Field(..., ge=0.0)
    active: bool = Field(default=True)
    id: Optional[UUID] = None

    def to_account(self) -> "Account":
        return Account.create(
            alias=self.alias,
            name=self.name,
            symbol=self.symbol,
            balance=self.balance,
            active=self.active,
            aggregate_id=self.id,
        )


@openapi.component
class AccountOut(Base):
    alias: str = Field(..., min_length=8, max_length=50)
    name: str = Field(..., min_length=5, max_length=100)
    symbol: str
    balance: float = Field(..., ge=0.0)
    active: bool
    id: UUID
    created_at: datetime

    @staticmethod
    def from_account(account: Account) -> "AccountOut":
        return AccountOut(
            alias=account.alias,
            name=account.name,
            symbol=account.symbol,
            balance=account.balance,
            active=account.active,
            id=UUID(account.aggregate_id.value),
            created_at=account.created_at,
        )
