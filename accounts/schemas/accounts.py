from typing import List, Optional
from pydantic import Field, field_serializer
from accounts.schemas.base import BaseSchema
from sanic_ext import openapi


class AccountBase(BaseSchema):
    alias: str


@openapi.component
class AccountCreate(AccountBase):
    name: str
    active: bool = Field(default=True)
    balance: float = Field(default=0.0)
    symbol: str


@openapi.component
class AccountUpdate(BaseSchema):
    alias: Optional[str] = None
    name: Optional[str] = None
    active: Optional[bool] = None
    balance: Optional[float] = None  # for DEBUG purposes
    symbol: Optional[str] = None


@openapi.component
class Account(AccountBase):
    id: str
    name: str
    active: bool
    balance: float
    symbol: str

    @field_serializer("id")
    def serialize_id(self, value):
        return str(value)


@openapi.component
class AccountList(BaseSchema):
    accounts: List[Account]
