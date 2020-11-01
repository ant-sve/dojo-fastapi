from pydantic import BaseModel

from typing import Any

EXCLUDE_FIELDS = {'pk', }


class BaseBookSchema(BaseModel):
    author: str
    title: str


class DBBookSchema(BaseBookSchema):
    pk: Any

    class Config:
        fields = {'pk': '_id'}


class ResponseCreateSchema(BaseModel):
    inserted: bool


class ResponseUpdateSchema(BaseModel):
    modified: int


class ResponseRemoveSchema(BaseModel):
    removed: int
