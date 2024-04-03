from typing import Any, Dict
from petisco import DomainEvent, DomainError


class TransactionReceived(DomainEvent):
    data: Dict[str, Any]


class TransactionCreated(DomainEvent):
    data: Dict[str, Any]


class TransactionRetrieved(DomainEvent): ...


class TransactionUpdated(DomainEvent):
    data: Dict[str, Any]


class TransactionDeleted(DomainEvent):
    data: Dict[str, Any]


class TransactionApproved(DomainEvent):
    data: Dict[str, Any]


class TransactionRejected(DomainEvent):
    data: Dict[str, Any]