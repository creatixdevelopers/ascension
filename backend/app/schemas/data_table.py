from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class DataTableSchema(BaseModel):
    skip: int = 0
    limit: int = 10
    order: list
    search: str | None = ""
    filters: list


class DataTableResponseSchema(BaseModel, Generic[T]):
    data: list[T]
    filtered: int
    total: int
