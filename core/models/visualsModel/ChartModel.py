from pydantic import BaseModel,Field
from typing import List, Optional, Literal, Any
from core.models.visualsModel.ValueObject import DisplayObj
import uuid

# Data Transfer Objects
class YAxisSeriesModel(BaseModel):
    Title: str
    Type: str
    UnitType: Optional[DisplayObj] = DisplayObj.empty
    Symbol: str
    AreaFill: Optional[bool] = False
    Values: List[float]

    YaxisId: Optional[str] = "left"  # ---------


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


# ---------
class YaxisControllerModel(BaseModel):
    Id: Optional[str] = "left"
    Orientation: Optional[str] = "left"
    Unit: Optional[str] = "$"


class ChartDataModel(BaseModel):
    Id: str
    Title: str
    Xaxis: List[str]
    YaxisSeries: List[YAxisSeriesModel]
    IndexAxis: str
    RightYaxis: bool
    YaxisController: List[YaxisControllerModel]
    Markers: Optional[List[MarkerModel]] = []
    Visibility: Optional[bool] = True
    Type: Optional[str] = "Normal"
    KpiType : Optional[Literal["Actuals","Custom","Budget"]] = "Actuals"


class ChartsListModel(BaseModel):
    Charts: List[ChartDataModel]


# Request Body
class MetricRequestModel(BaseModel):
    Label: str
    FunctionName: str


class ChartRequestBody(BaseModel):
    Year: int
    Months: List[int]
    Title: str
    Metrics: List[MetricRequestModel]
