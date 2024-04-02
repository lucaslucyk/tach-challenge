import datetime as dt
from uuid import UUID
from petisco import AggregateRoot, Uuid
from pydantic import Field, validator


class Transaction(AggregateRoot):
    source_account_id: UUID
    target_account_id: UUID
    symbol: str
    amount: float

    @validator("aggregate_id", pre=True, always=True)
    def set_aggregate_id(cls, v):
        return v or Uuid.v4()

    @staticmethod
    def create(
        source_account_id: UUID,
        target_account_id: UUID,
        symbol: str,
        amount: float,
        aggregate_id: Uuid | None = None,
    ):
        return Transaction(
            source_account_id=source_account_id,
            target_account_id=target_account_id,
            symbol=symbol,
            amount=amount,
            aggregate_id=aggregate_id,
        )
