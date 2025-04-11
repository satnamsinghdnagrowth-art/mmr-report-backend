from helper.readExcel import readExcelFile
from datetime import datetime
from services.coa.RetrieveAccountNames import retriveAccountNames
from services.coa.RetriveAccountValues import retriveAccountValues
from services.balancesheet.RetrieveBSAccountName import retriveBSAccountNames
from services.balancesheet.RetreiveBSAccountValues import retriveBSAccountValues
from services.calculations.revenueCalculation import calculateRevenue

from services.kpis.getKPIsNames import retriveKPIsNames
from core.models.base.ResultModel import Result


# Analyze the data
def retriveNames():
    try:
        data = {
            "KPIs": retriveKPIsNames().Data,
            "IncomeStatements": retriveBSAccountNames(category="BALANCE SHEET").Data,
            "BalanceSheet": retriveBSAccountNames(category="PROFIT & LOSS").Data,
            "Chart of Accounts": retriveAccountNames().Data,
        }
        return Result(Data=data, Status=1, Message="Success")

    except Exception as ex:
        message = f"Error occur at readExcelFile: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
