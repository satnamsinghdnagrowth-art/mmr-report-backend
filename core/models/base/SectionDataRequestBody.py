from pydantic import BaseModel
from typing import List, Optional, Literal


class SectionRequestData(BaseModel):
    Year: int
    Months: List[int]
    CompanyId: Optional[int] = 123456
    ReportType: Literal["Year", "Month", "Quarter"]
    SectionName: str
