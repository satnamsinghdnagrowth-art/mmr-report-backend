from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Report Model
class ReportModel(BaseModel):
    Id: int = Field(default=None, alias="_id")
    ReportName: str
    UserId: Optional[int] = 123
    CompanyId: Optional[int] = 111
    ReportExcelFile: str
    ReportJsonFile: str
    CreatedOn: Optional[datetime] = datetime.now()
    UpdatedOn: Optional[datetime] = datetime.now()
    CreatedBy: Optional[int] = 123
    UpdatedBy: Optional[int] = 123
