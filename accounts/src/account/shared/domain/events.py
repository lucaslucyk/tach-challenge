from typing import Any, Dict
from petisco import DomainEvent, DomainError


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


class FundsError(DomainEvent):
    trigger: Dict[str, Any]


class AccountNotFound(FundsError):
    account_id: str


class AccountNotAvailable(FundsError):
    account_id: str


class SymbolError(FundsError):
    source_symbol: str
    target_symbol: str


class InsufficientFunds(FundsError):
    account_id: str


class IncompleteTransaction(FundsError): ...
