from datetime import datetime
from typing import List, Optional, Tuple
from uuid import UUID
from pydantic import BaseModel, Field
from sanic_ext import openapi
from accounts.src.transaction.shared.domain.transaction import TransactionStatus
from transactions.src.transaction.shared.domain.transaction import Transaction


class Base(BaseModel):
    class Config:
        extra = "ignore"


@openapi.component
class TransactionIn(Base):
    source_account_id: UUID
    target_account_id: UUID
    symbol: str
    amount: float = Field(..., ge=0.0)
    id: Optional[UUID] = None

    def to_transaction(self) -> "Transaction":
        return Transaction.create(
            source_account_id=self.source_account_id,
            target_account_id=self.target_account_id,
            symbol=self.symbol,
            amount=self.amount,
            aggregate_id=self.id,
        )


@openapi.component
class TransactionOut(Base):
    source_account_id: UUID
    target_account_id: UUID
    symbol: str
    amount: float = Field(..., ge=0.0)
    status: TransactionStatus
    id: UUID
    created_at: datetime

    @staticmethod
    def from_transaction(transaction: Transaction) -> "TransactionOut":
        return TransactionOut(
            source_account_id=transaction.source_account_id,
            target_account_id=transaction.target_account_id,
            symbol=transaction.symbol,
            amount=transaction.amount,
            status=transaction.status,
            id=UUID(transaction.aggregate_id.value),
            created_at=transaction.created_at,
        )


@openapi.component
class TransactionList(Base):
    transactions: List[TransactionOut]

    @staticmethod
    def from_transactions(transactions: List[Transaction]) -> "TransactionList":
        return TransactionList(
            transactions=[TransactionOut.from_transaction(transaction) for transaction in transactions]
        )


@openapi.component
class Paginator(BaseModel):
    limit: Optional[int] = None
    skip: Optional[int] = None
    sort: Optional[List[Tuple[str, int]]] = None
