from meiga import Result, Success
from sanic import NotFound
from beanie_crud.crud import CRUDBase
from accounts.models.accounts import Account as AccountModel
from accounts.schemas.accounts import AccountCreate, AccountUpdate


class CRUDAccount(CRUDBase[AccountModel, AccountCreate, AccountUpdate]):
    document = AccountModel

    async def get_by_alias(self, alias: str) -> Result[AccountModel, NotFound]:
        result = await self.find_one(self.document.alias == alias)
        if result.is_failure:
            return result

        return Success(result.get_value())


accounts = CRUDAccount()
