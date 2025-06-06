from pydantic import BaseModel


class DateObject(BaseModel):
    Month: int

    Year: int


class TimeValueObject(BaseModel):
    Month: int
    Year: int
    Value: float


class ReportDescriptionsModel(BaseModel):
    ReportName: str
    FinancialYear: str
    DataRange: list[DateObject]
