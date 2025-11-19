from typing import TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")


class Result(BaseModel):
    Data: Optional[T] = None
    Status: int
    Message: str
