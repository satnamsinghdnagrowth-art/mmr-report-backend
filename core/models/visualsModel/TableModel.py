from pydantic import BaseModel
from typing import List

# Data Transfer Objects
class TableModel(BaseModel):
    Title : str
    Column: List[str]             
    Rows: List[List[str]]     