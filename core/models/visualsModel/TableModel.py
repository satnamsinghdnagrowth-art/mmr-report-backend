from pydantic import BaseModel
from typing import List, Any,Optional
from enum import Enum

class TableTypesName(Enum):
    Tabular : str = "Tabular"
    Progress : str = "Progress"


# Data Transfer Objects
class TableModel(BaseModel):
    Title: str
    Column: List[str]
    Rows: List[List[Any]]
    TableType : Optional[str] = TableTypesName.Tabular.value
    Visibility : Optional[bool] = True


class TableListModel(BaseModel):
    Tables: List[TableModel]
