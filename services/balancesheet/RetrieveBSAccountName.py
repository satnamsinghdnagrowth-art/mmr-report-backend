from helper.readExcel import readExcelFile
from datetime import datetime
from collections import defaultdict
from config.variable import variableMapping
from core.models.Accounts.AccountNameResponseModel import AccountNameModel
from core.models.base.ResultModel import Result


# Analyze the data
def retriveBSAccountNames(category : str):
    try:

        result = defaultdict(list)

        BSData = variableMapping[category]

        for main, category in BSData.items():

            for code in category:
                    
                result[main].append(
                    AccountNameModel(
                        Name=list(code.values())[0], Code=list(code.keys())[0]
                    )
                )

        return Result(Data=result, Status=1, Message="Success")

    except Exception as ex:
        message = f"Error occur at readExcelFile: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
