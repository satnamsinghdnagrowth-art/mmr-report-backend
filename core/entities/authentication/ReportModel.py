from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Report Model
class ReportModel(BaseModel):
    Id: int = Field(default=None, alias="_id")
    ReportName: Optional[int] = Field(default=123, alias="report_name")
    Description: str = Field(default=123, alias="description")
    CreatedOn: Optional[datetime] = datetime.now()
    UpdatedOn: Optional[datetime] = datetime.now()
    CreatedBy: Optional[int] = 123
    UpdatedBy: Optional[int] = 123
