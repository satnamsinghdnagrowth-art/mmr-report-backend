from pydantic import BaseModel
from typing import List, Literal, Optional


# Section Data
class CustomKpiRequestModel(BaseModel):
    VisualType: Literal["Table", "Chart", "Card"]
    Items: List[str]
    SectionName: str
    SectionId: Optional[str] = None  # Optional for backwards compatibility


class CustomKpiCreationModel(BaseModel):
    VisualType: Literal["Table", "Chart", "Card"]
    Year: int
    Months: List[int]
    Items: List[str]
