from petisco import Uuid


class AccountJsonMother:
    @staticmethod
    def any(
        name: str = "string",
        alias: str = "stringstring",
        symbol: str = "string",
        balance: float = 100.0,
        active: bool = True,
    ) -> dict:
        return {
            "name": name,
            "alias": alias,
            "symbol": symbol,
            "balance": balance,
            "active": active,
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        }

    @staticmethod
    def with_id(id: str) -> dict:
        return {
            "name": "string",
            "alias": "stringstring",
            "symbol": "string",
            "balance": 100.0,
            "active": True,
            "id": id,
        }

    @staticmethod
    def random() -> dict:
        return {
            "name": "string",
            "alias": "stringstring",
            "symbol": "string",
            "balance": 100.0,
            "active": True,
            "id": Uuid.v4().value,
        }

    @staticmethod
    def without_id(
        name: str = "string",
        alias: str = "stringstring",
        symbol: str = "string",
        balance: float = 100.0,
        active: bool = True,
    ) -> dict:
        return {
            "name": name,
            "alias": alias,
            "symbol": symbol,
            "balance": balance,
            "active": active,
        }

    @staticmethod
    def invalid() -> dict:
        return {}
