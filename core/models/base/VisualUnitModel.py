from pydantic import BaseModel
from typing import Literal


class UnitModel(BaseModel):
    type :Literal["percentage","currency"]
    symbol : str