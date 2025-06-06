from datetime import datetime
from services.accountNames.RetrieveCOANames import retriveCOANames
from services.accountNames.RetrieveBSAccountName import retriveBSAccountNames
from services.accountNames.RetrieveKPIsNames import retriveKPIsNames
from core.models.base.ResultModel import Result


# Analyze the data
def retreiveFinacialsNames(year: int, month: int,reportId:int):
    try:
        data = {
            "KPIs": retriveKPIsNames(year, month).Data,
            "PROFIT & LOSS": retriveBSAccountNames(
                year, month, category="PROFIT & LOSS"
            ).Data,
            "BalanceSheet": retriveBSAccountNames(
                year, month, category="BALANCE SHEET"
            ).Data,
            "Chart of Accounts": retriveCOANames(year, month,reportId).Data,
        }

        return Result(Data=data, Status=1, Message="Success")

    except Exception as ex:
        message = f"Error occur at retreiveNames: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
