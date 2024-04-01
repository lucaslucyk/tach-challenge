import datetime as dt
from petisco import AggregateRoot, Uuid
from pydantic import Field, validator

from accounts.src.account.shared.domain.events import AccountCreated


class Account(AggregateRoot):
    alias: str = Field(..., min_length=8, max_length=50)
    name: str = Field(..., min_length=5, max_length=100)
    symbol: str
    balance: float = Field(..., ge=0.0)
    active: bool = Field(default=True)
    created_at: dt.datetime | None = None

    @validator("aggregate_id", pre=True, always=True)
    def set_aggregate_id(cls, v):
        return v or Uuid.v4()

    @validator("created_at", pre=True, always=True)
    def set_created_at(cls, v):
        return v or dt.datetime.utcnow()

    @staticmethod
    def create(
        alias: str,
        name: str,
        symbol: str,
        balance: float,
        active: bool = True,
        aggregate_id: Uuid | None = None,
    ):
        account = Account(
            alias=alias,
            name=name,
            symbol=symbol,
            balance=balance,
            active=active,
            aggregate_id=aggregate_id,
        )
        account.record(AccountCreated())
        return account
