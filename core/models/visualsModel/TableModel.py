from pydantic import BaseModel
from typing import List, Any


# Data Transfer Objects
class TableModel(BaseModel):
    Title: str
    Column: List[str]
    Rows: List[List[Any]]
