from pydantic import BaseModel
from typing import List,Optional


class SectionChartRequestData(BaseModel):
    Year: int
    Months: List[int]
    CompanyId : Optional[int] = 123456
    ReportType: str
    SectionName: str
