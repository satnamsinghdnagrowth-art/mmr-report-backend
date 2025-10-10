from pydantic import BaseModel
from typing import List, Literal, Optional


# Section Data
class CustomKpiRequestModel(BaseModel):
    VisualType: Literal["Table", "Chart"]
    VisualSubType: Optional[Literal["Set"]] = "Set"
    StartMonth: int
    EndMonth: int
    Items: List[str]
