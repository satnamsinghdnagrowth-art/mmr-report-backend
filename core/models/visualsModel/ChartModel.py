from pydantic import BaseModel
from typing import List


# Data Transfer Objects
class YAxisSeriesModel(BaseModel):
    Title: str
    Type: str
    Values: List[float]


class ChartDataModel(BaseModel):
    Title: str
    Xaxis: List[str]
    YaxisSeries: List[YAxisSeriesModel]
    IndexAxis: str


# Request Body
class MetricRequestModel(BaseModel):
    Label: str
    FunctionName: str


class ChartRequestBody(BaseModel):
    Year: int
    Months: List[int]
    Title: str
    Metrics: List[MetricRequestModel]
