from pydantic import BaseModel
from typing import List


class SectionChartRequestData(BaseModel):
    Year: int
    Months: List[int]
    ReportType: str
    SectionName: str
