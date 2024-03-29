from pydantic import BaseModel, field_serializer


class BaseSchema(BaseModel): ...

    # @field_serializer('id')
    # def serialize_id(self, value):
    #     return str(value)