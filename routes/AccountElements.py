from fastapi import APIRouter
from services.coa.RetrieveAccountNames import retriveAccountNames
from services.coa.RetriveAccountValues import retriveAccountValues
from services.balancesheet.RetrieveBSAccountName import retriveBSAccountNames
from services.balancesheet.RetreiveBSAccountValues import retriveBSAccountValues
from services.calculations.revenueCalculation import calculateRevenue
from services.GetAccountNames import retriveNames
from services.kpis.getKPIsNames import retriveKPIsNames
from core.models.base.ResultModel import Result

Account = APIRouter()

# Get COA Variables Names
@Account.get("/COA/get/Names")
def getCOANames() -> Result:
    return retriveNames()
    # return retriveAccountNames()


# Get COA Variables Values
@Account.get("/COA/get/Values")
def getCOAValues(accountName : str) -> Result:
    return retriveAccountValues(accountName)


# Get Balance Sheet Variables Names
@Account.get("/Balancesheet/get/Names")
def getBalancesheetVariableNames() -> Result:
    return retriveBSAccountNames(category="BALANCE SHEET")


# Get Balance Sheet variable Values
@Account.get("/Balancesheet/get/Values")
def getBalancesheetVariableValues(accountName: str) -> Result:
    return retriveBSAccountValues(accountName)


# Get Income Statement Variables Names
@Account.get("/IncomeStatement/get/Names")
def getIncomeStatementVariableNames() -> Result:
    return retriveBSAccountNames(category="PROFIT & LOSS")


# Get Income Statement Varbales Values
@Account.get("/IncomeStatement/get/Values")
def getIncomeStatementVariableValues(accountName: str) -> Result:
    return retriveBSAccountValues(accountName)


# Get KPIs variable Values
@Account.get("/KPIs/get/Names")
def getKPIsNames() -> Result:
    return retriveKPIsNames()


# Get KPIs variable Values
@Account.get("/KPIs/get/Values")
def getKPIsValues() -> Result:
    return calculateRevenue()