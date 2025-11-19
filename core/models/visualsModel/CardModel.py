from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from core.models.visualsModel.ValueObject import ValueObjectModel
import uuid


# Data Transfer Objects
class TrendLineChart(BaseModel):
    Xaxis: List[str]
    Yaxis: List[float]
    Visibility: Optional[bool] = True


class FooterModel(BaseModel):
    ComparisonValue: ValueObjectModel
    ComparisonText: str
    TrendLine: Optional[TrendLineChart] = None
    Visibility: Optional[bool] = True


class CardDataModel(BaseModel):
    Id: str
    Title: str
    Content: ValueObjectModel
    Footer: FooterModel
    Visibility: Optional[bool] = True
    KpiType: Optional[Literal["Actuals", "Custom", "Budget"]] = "Actuals"


class CardsListModel(BaseModel):
    Cards: List[CardDataModel]


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
