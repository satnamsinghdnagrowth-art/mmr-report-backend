from fastapi import APIRouter
from core.models.base.DateFilterModel import DateFilter
from core.models.base.ResultModel import Result

PermissionRouter = APIRouter()


# Get  Account Names
@PermissionRouter.get("/create/user", response_model=Result)
def createUser() -> Result:
    return permissionCreation(year, month, reportId)
