from typing import Any, Dict, Optional
from petisco import DomainEvent

from accounts.src.transaction.shared.domain.transaction import Transaction


class TransactionCreated(DomainEvent):
    data: Optional[Dict[str, Any]] = None

    def to_transaction(self):
        return Transaction(
            source_account_id=self.data.get("source_account_id", None),
            target_account_id=self.data.get("target_account_id", None),
            symbol=self.data.get("symbol", None),
            amount=self.data.get("amount", None),
            aggregate_id=self.data.get("aggregate_id", None),
        )


class TransactionUpdated(TransactionCreated):
    ...