from pydantic import BaseModel
from typing import Optional, Any
from enum import Enum


class DisplayObj(str, Enum):
    currency = "currency"
    percentage = "percentage"
    months='months'
    empty = ""


# Value Object
class ValueObjectModel(BaseModel):
    Value: Any
    isPositive: bool
    Type: Optional[DisplayObj] = DisplayObj.empty
    Symbol: Optional[str] = ""
