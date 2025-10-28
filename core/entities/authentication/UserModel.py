from pydantic import BaseModel, Field, validator
from typing import Optional,Literal
from datetime import datetime
import re

# Report Model
class UserRegistrationModel(BaseModel):
    Id: int 
    FirstName: str
    LastName: str
    Email: str
    ContactNumber: str
    Password: str
    CreatedOn: datetime = Field(default_factory=datetime.utcnow)
    UpdatedOn: datetime = Field(default_factory=datetime.utcnow)

# Roles Model
class Role(BaseModel):
    Id : int
    RoleName : Literal["Admin","Superuser","Analyst"]
    Description : str
    CreatedOn: datetime = Field(default_factory=datetime.utcnow)
    UpdatedOn: datetime = Field(default_factory=datetime.utcnow)
    CreatedBy: Optional[int] = None
    UpdatedBy: Optional[int] = None

# PermissionModel
class Permission(BaseModel):
    Id : int
    Code : Literal["can_create","can_update","can_edit","can_delete"]
    Description: str
    CreatedOn: datetime = Field(default_factory=datetime.utcnow)
    UpdatedOn: datetime = Field(default_factory=datetime.utcnow)
    CreatedBy: Optional[int] = None
    UpdatedBy: Optional[int] = None

# User Role Model
class UserRole(BaseModel):
    Id : int
    UserId : int
    RoleId : int
    CreatedOn: datetime = Field(default_factory=datetime.utcnow)
    UpdatedOn: datetime = Field(default_factory=datetime.utcnow)
    CreatedBy: Optional[int] = None
    UpdatedBy: Optional[int] = None

# Role Permission Model
class RolePermission(BaseModel):
    Id:int
    RoleId : int
    PermissionId : int
    CreatedOn: datetime = Field(default_factory=datetime.utcnow)
    UpdatedOn: datetime = Field(default_factory=datetime.utcnow)
    CreatedBy: Optional[int] = None
    UpdatedBy: Optional[int] = None


class UserLoginModel(BaseModel):
    Email: str
    Password: str
