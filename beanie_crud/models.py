from typing import TypeVar
from pydantic import BaseModel
from beanie import Document
from pydantic import BaseModel


class ModelBase(Document, BaseModel): ...


DocumentType = TypeVar("DocumentType", bound=ModelBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
