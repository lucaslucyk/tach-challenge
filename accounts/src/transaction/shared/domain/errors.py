from petisco import Uuid
from petisco.base.domain.errors.domain_error import DomainError


class SymbolMatchError(DomainError):
    
    def __init__(self, message: str):
        super().__init__(additional_info={"message": message})


class FundsError(DomainError):
    
    def __init__(self, account_id: Uuid):
        message = f"Account {account_id} does not have enough funds."
        super().__init__(additional_info={"message": message})


class DeductionError(DomainError):
    
    def __init__(self, account_id: Uuid, amount: float):
        message = f"Cannot deduct {amount} from account {account_id}."
        super().__init__(additional_info={"message": message})