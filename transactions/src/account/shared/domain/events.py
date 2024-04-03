from typing import Any, Dict
from petisco import DomainEvent


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
