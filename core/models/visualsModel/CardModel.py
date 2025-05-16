from pydantic import BaseModel
from typing import List, Optional
from core.models.visualsModel.ValueObject import ValueObjectModel


# Data Transfer Objects
class TrendLineChart(BaseModel):
    Xaxis: List[str]
    Yaxis: List[float]


class FooterModel(BaseModel):
    ComparisonValue: ValueObjectModel
    ComparisonText: str
    TrendLine: Optional[TrendLineChart]


class CardDataModel(BaseModel):
    Title: str
    Content: ValueObjectModel
    Footer: FooterModel


# Request Body
class TrendRequestBody(BaseModel):
    FunctionName: str
    ComparedTo: str


class CardRequestBody(BaseModel):
    Title: str
    Year: int
    Month: List[int]
    FuntionName: str
    Trend: TrendRequestBody
