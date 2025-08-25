from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Report Model
class CompanyModel(BaseModel):
    Id: int = Field(default=None, alias="_id")
    UserId: Optional[int] = 123
    CompanyName: str
    BusinessType: str
    Industry: str
    CreatedOn: Optional[datetime] = datetime.now()
    UpdatedOn: Optional[datetime] = datetime.now()
    CreatedBy: Optional[int] = 123
    UpdatedBy: Optional[int] = 123
