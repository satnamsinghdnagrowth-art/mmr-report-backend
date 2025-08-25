from pydantic import BaseModel
from typing import List, Any,Optional


# Data Transfer Objects
class TableModel(BaseModel):
    Title: str
    Column: List[str]
    Rows: List[List[Any]]
    Visibility : Optional[bool] = True


class TableListModel(BaseModel):
    Tables: List[TableModel]
