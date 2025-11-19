from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Report Model
class CompanyModel(BaseModel):
    Id: int = Field(default=None, alias="_id")
    UserId: Optional[int] = Field(default=123, alias="user_id")
    CompanyName: str = Field(default=123, alias="company_name")
    Industry: Optional[str] = Field(default=123, alias="industry")
    Description: str = Field(default=123, alias="description")
    CreatedOn: Optional[datetime] = datetime.now()
    UpdatedOn: Optional[datetime] = datetime.now()
    CreatedBy: Optional[int] = 123
    UpdatedBy: Optional[int] = 123
