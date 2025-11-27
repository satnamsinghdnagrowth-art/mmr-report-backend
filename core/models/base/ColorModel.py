from pydantic import BaseModel
from typing import Optional
from enum import Enum

COLORS = ["#8FBFD9", "#C8D1D8", "#EA7F8B"]

class ColorsModel(BaseModel):
    FillLight : Optional[str] = COLORS[0]
    FillDark : Optional[str] = COLORS[1]




class ChartColorModel(BaseModel):
    Title : Optional[str] = "red"
    Label : Optional[str] = "red"
    Xaxis : Optional[str] = "red"
    Yaxis : Optional[str] = "red"
    Series : Optional[str] = "red"
