from datetime import datetime
from services.AccountValues.RetriveAccountsValue import retriveBSAccountValues
from services.AccountValues.RetriveCOAValues import retriveCOAValues
from core.models.base.ResultModel import Result
import json 


# Analyze the data
def retreiveFinacialsValues():
    try:
        # data = {
        #     "IncomeStatements": retriveBSAccountValues(category="PROFIT & LOSS").Data,
        #     "BalanceSheet":retriveBSAccountValues(category="BALANCE SHEET").Data,
        #     "Chart of Accounts": retriveCOAValues().Data,
        # }


        data = {
            "IncomeStatements": retriveCOAValues(category="PROFIT & LOSS").Data,
            "BalanceSheet":retriveCOAValues(category="BALANCE SHEET").Data,
        }


        # with open("config/FileOutputTest.json", "w") as f:
        #     json.dump(data, f, indent=4)

        return Result(Data=data, Status=1, Message="Success")

    except Exception as ex:
        message = f"Error occur at retreiveNames: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
