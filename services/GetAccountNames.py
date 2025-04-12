from datetime import datetime
from services.RetrieveAccountNames import retriveAccountNames
from services.RetrieveBSAccountName import retriveBSAccountNames
from services.RetrieveKPIsNames import retriveKPIsNames
from core.models.base.ResultModel import Result


# Analyze the data
def retreiveNames():
    try:
        data = {
            "KPIs": retriveKPIsNames().Data,
            "IncomeStatements": retriveBSAccountNames(category="BALANCE SHEET").Data,
            "BalanceSheet": retriveBSAccountNames(category="PROFIT & LOSS").Data,
            "Chart of Accounts": retriveAccountNames().Data,
        }

        return Result(Data=data, Status=1, Message="Success")

    except Exception as ex:
        message = f"Error occur at retreiveNames: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
