from pydantic import BaseModel
from typing import List, Optional

# Data Transfer Objects
class TrendLineChart(BaseModel):
    Xaxis: List[str]             
    Yaxis: List[float]      


class CardDataModel(BaseModel):
    Title: str                     
    Content : str
    ComparisonValue : str
    ComparisonText : str
    TrendLine: Optional[TrendLineChart]    


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