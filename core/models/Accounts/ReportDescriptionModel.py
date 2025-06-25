from pydantic import BaseModel
from typing import Optional


class DateObject(BaseModel):
    Month: int

    Year: int


class TimeValueObject(BaseModel):
    Month: int
    Year: int
    Value: float


class ReportDescriptionsModel(BaseModel):
    ReportName: str
    FinancialYear: int
    DataRange: list[DateObject]
    CompanyLogoPath : Optional[str] = None

