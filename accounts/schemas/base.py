from pydantic import BaseModel, field_serializer


class BaseSchema(BaseModel):

    class Config:
        extra = "ignore"

    # @field_serializer('id')
    # def serialize_id(self, value):
    #     return str(value)