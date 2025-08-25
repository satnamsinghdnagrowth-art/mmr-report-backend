from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
import re


# Report Model
class UserRegistrationModel(BaseModel):
    Id: int = Field(default=None, alias="_id")
    FirstName: str
    LastName: str
    Email: str
    ContactNumber: str
    Password: int

    @validator("ContactNumber")
    def validate_contact_number(cls, value):
        pattern = r"^\+?[0-9\s\-()]{10,20}$"
        if not re.fullmatch(pattern, value):
            raise ValueError("Invalid phone number format")
        return value


class UserLoginModel(BaseModel):
    Email: str
    Password: str
