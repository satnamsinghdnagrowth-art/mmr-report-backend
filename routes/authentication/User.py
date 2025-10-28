from fastapi import APIRouter
from core.models.base.DateFilterModel import DateFilter
from core.models.base.ResultModel import Result

UserRouter = APIRouter()

# Get  Account Names
@UserRouter.get("/create/user", response_model=Result)
def createUser() -> Result:
    return userCreation(year, month, reportId)

