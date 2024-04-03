from datetime import datetime
from enum import Enum
from typing import Annotated
from uuid import UUID, uuid4

from beanie import Indexed
from petisco import Uuid
from pydantic import Field
import pymongo
from petisco_sanic.extra.beanie.document.document_base import DocumentBase
from transactions.src.transaction.shared.domain.transaction import Transaction


class TransactionStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class DocumentTransaction(DocumentBase[Transaction]):

    # beanie
    id: UUID = Field(default_factory=uuid4)
    aggregate_id: Annotated[str, Indexed(str, unique=True)]
    source_account_id: UUID
    target_account_id: UUID
    symbol: str
    amount: float = Field(..., ge=0.0)
    status: TransactionStatus = Field(default=TransactionStatus.PENDING)
    created_at: datetime | None = Field(default_factory=datetime.now)

    class Settings:
        name = "transactions"
        indexes = [
            [
                ("aggregate_id", pymongo.TEXT),
            ],
        ]

    def to_domain(self) -> Transaction:
        return Transaction(
            source_account_id=self.source_account_id,
            target_account_id=self.target_account_id,
            symbol=self.symbol,
            amount=self.amount,
            status=self.status,
            aggregate_id=Uuid(self.aggregate_id),
            created_at=self.created_at,
        )

    @staticmethod
    def from_domain(transaction: Transaction) -> "DocumentTransaction":
        return DocumentTransaction(
            source_account_id=transaction.source_account_id,
            target_account_id=transaction.target_account_id,
            symbol=transaction.symbol,
            amount=transaction.amount,
            status=transaction.status or TransactionStatus.PENDING,
            aggregate_id=Uuid(transaction.aggregate_id),
            created_at=transaction.created_at,
        )
