from datetime import datetime
from config.variable import variableMapping
from core.models.base.ResultModel import Result


def retriveKPIsNames():
    try:
        resultDict = {
            "PROFITIABILITY" :[
            {"Name": "TotalRevenue", "Code": "TotalRevenue"}
            ]
        }

        return Result(
            Data=resultDict,
            Status=1,
            Message="KPIs Name retrieve Succesfully",
        )

    except Exception as ex:
        message = f"Error occur at calculateRevenue: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
