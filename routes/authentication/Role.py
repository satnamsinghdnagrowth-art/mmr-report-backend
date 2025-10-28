from fastapi import APIRouter
from core.models.base.DateFilterModel import DateFilter
from core.models.base.ResultModel import Result

RoleRouter = APIRouter()

# Get  Account Names
@RoleRouter.get("/create/role", response_model=Result)
def createRole() -> Result:
    return roleCreation(year, month, reportId)

