from fastapi import APIRouter
from services.coa.RetrieveAccountNames import retriveAccountNames
from services.coa.RetriveAccountValues import retriveAccountValues
from services.balancesheet.RetrieveBSAccountName import retriveBSAccountNames
from core.models.base.ResultModel import Result


Account = APIRouter()

# Get COA Variables Names
@Account.get("/COA/get/Names")
def getCOANames() -> Result:
    return retriveAccountNames()


# Get COA Variables Values
@Account.get("/COA/get/Values")
def getCOAValues(accountName : str) -> Result:
    return retriveAccountValues(accountName)


# Get Balance Sheet Variables Names
@Account.get("/Balancesheet/get/Names")
def getBalancesheetVariableNames() -> Result:
    return retriveBSAccountNames()


# Get Balance Sheet variable Values
@Account.get("Balancesheet/get/Values")
@Account.get("/get/Values")
def getBalancesheetVariableValues(accountName: str) -> Result:
    return retriveAccountValues(accountName)
