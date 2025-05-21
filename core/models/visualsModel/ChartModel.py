from pydantic import BaseModel
from typing import List, Optional, Literal, Any
from core.models.visualsModel.ValueObject import DisplayObj


# Data Transfer Objects
class YAxisSeriesModel(BaseModel):
    Title: str
    Type: str
    UnitType: Optional[DisplayObj] = DisplayObj.empty
    Symbol: str
    AreaFill: Optional[bool] = False
    Values: List[float]
    # BarTypes: Optional[List[Literal["relative", "total", "subtotal"]]] = None  # Add this for waterfall chart


class MarkerModel(BaseModel):
    Label: str
    Xvalue: float  # match Xaxis label
    Yvalue: float
    Color: str
    Shape: Optional[Literal["circle", "square", "diamond", "triangle", "bullseye"]] = (
        "circle"
    )
    Size: Optional[int] = 8
    Description: Optional[Any] = None


class ChartDataModel(BaseModel):
    Title: str
    Xaxis: List[str]
    YaxisSeries: List[YAxisSeriesModel]
    IndexAxis: str
    RightYaxis: bool
    Markers: Optional[List[MarkerModel]] = []


# Request Body
class MetricRequestModel(BaseModel):
    Label: str
    FunctionName: str


class ChartRequestBody(BaseModel):
    Year: int
    Months: List[int]
    Title: str
    Metrics: List[MetricRequestModel]
