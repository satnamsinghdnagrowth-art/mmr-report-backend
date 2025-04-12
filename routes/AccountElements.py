from fastapi import APIRouter
from services.GetAccountNames import retreiveNames
from services.ExtractDataRange import retriveDataRange
from core.models.base.ResultModel import Result

Account = APIRouter()

# Get  Account Names and Values
@Account.get("/get/Names")
def getAccountNames() -> Result:
    return retreiveNames()


# Get  Account Names and Values
@Account.get("/get/reportDescription")
def getReportDescription() -> Result:
    return retriveDataRange()

