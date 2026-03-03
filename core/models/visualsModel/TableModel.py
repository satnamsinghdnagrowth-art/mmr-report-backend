from pydantic import BaseModel, Field
from typing import List, Any, Optional, Literal
from enum import Enum
import uuid
from core.models.base.ColorModel import COLORS,ColorsModel

class TableTypesName(Enum):
    Tabular: str = "Tabular"
    Progress: str = "Progress"
    Variance: str = "Variance"


# Data Transfer Objects
class TableModel(BaseModel):
    Id: str
    Title: str
    Column: List[str]
    Rows: List[List[Any]]
    TableType: Optional[str] = TableTypesName.Tabular.value
    Visibility: Optional[bool] = True
    Colors : Optional[ColorsModel]= ColorsModel()
    KpiType: Optional[Literal["Actuals", "Custom", "Budget"]] = "Actuals"
    SectionID: Optional[str] = None
    PageNo: Optional[int] = None
    Order: Optional[int] = None


class TableListModel(BaseModel):
    Tables: List[TableModel]
