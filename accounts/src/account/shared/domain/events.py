from typing import Any, Dict
from petisco import DomainEvent


class AccountReceived(DomainEvent):
    data: Dict[str, Any]


class AccountCreated(DomainEvent):
    data: Dict[str, Any]


class AccountRetrieved(DomainEvent): ...


class AccountUpdated(DomainEvent):
    data: Dict[str, Any]


class AccountDeleted(DomainEvent):
    data: Dict[str, Any]


class FundsMoved(DomainEvent):
    trigger: Dict[str, Any]