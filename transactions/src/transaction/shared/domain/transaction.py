from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID
from petisco import AggregateRoot, Uuid
from pydantic import Field, validator

from transactions.src.transaction.shared.domain.events import (
    TransactionReceived,
)


class TransactionStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class Transaction(AggregateRoot):
    source_account_id: UUID
    target_account_id: UUID
    symbol: str
    amount: float
    status: TransactionStatus | None = None
    created_at: datetime | None = None

    @validator("aggregate_id", pre=True, always=True)
    def set_aggregate_id(cls, v):
        return v or Uuid.v4()

    @validator("created_at", pre=True, always=True)
    def set_created_at(cls, v):
        return v or datetime.utcnow()

    @staticmethod
    def create(
        source_account_id: UUID,
        target_account_id: UUID,
        symbol: str,
        amount: float,
        status: Optional[TransactionStatus] = None,
        aggregate_id: Uuid | None = None,
        aggregate_version: int | None = None,
        created_at: datetime | None = None,
    ):
        transaction = Transaction(
            source_account_id=source_account_id,
            target_account_id=target_account_id,
            symbol=symbol,
            amount=amount,
            status=status,
            aggregate_id=aggregate_id,
            aggregate_version=aggregate_version,
            created_at=created_at,
        )
        transaction.record(
            TransactionReceived(data=transaction.model_dump(mode="json"))
        )
        return transaction
