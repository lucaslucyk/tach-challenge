from petisco import Uuid

from accounts.src.account.shared.domain.account import Account


class AccountMother:
    @staticmethod
    def any(
        name: str = "MyAccountName",
        alias: str = "MyAccountAlias",
        symbol: str = "MyAccountSymbol",
        balance: float = 100.0,
        active: bool = True,
    ) -> Account:
        return Account.create(
            aggregate_id=Uuid("17b37cdc-027b-4fdb-bdbe-b72ced9744b9"),
            name=name,
            alias=alias,
            symbol=symbol,
            balance=balance,
            active=active,
        )

    @staticmethod
    def updated(
        name: str = "MyAccountName",
        alias: str = "MyAccountAlias",
        symbol: str = "MyAccountSymbol",
        balance: float = 100.0,
        active: bool = True,
    ) -> Account:
        return Account.update(
            aggregate_id=Uuid("17b37cdc-027b-4fdb-bdbe-b72ced9744b9"),
            name=name,
            alias=alias,
            symbol=symbol,
            balance=balance,
            active=active,
        )

    @staticmethod
    def random(
        name: str = "MyAccountName",
        alias: str = "MyAccountAlias",
        symbol: str = "MyAccountSymbol",
        balance: float = 100.0,
        active: bool = True,
    ) -> Account:
        return Account.create(
            aggregate_id=Uuid.v4(),
            name=name,
            alias=alias,
            symbol=symbol,
            balance=balance,
            active=active,
        )
