from pydantic import BaseModel
from typing import List, Literal, Optional


# Section Data
class CustomKpiRequestModel(BaseModel):
    model_config = {"extra": "ignore"}   # ignore unknown fields (forward-compat)

    VisualType: Literal["Table", "Chart", "Card"]
    Items: List[str]
    SectionName: str
    SectionId: Optional[str] = None   # Optional for backwards compatibility
    VisualId: Optional[str] = None    # Pre-generated visual ID for delete matching


class CustomKpiCreationModel(BaseModel):
    VisualType: Literal["Table", "Chart", "Card"]
    Year: int
    Months: List[int]
    Items: List[str]
    VisualId: Optional[str] = None
