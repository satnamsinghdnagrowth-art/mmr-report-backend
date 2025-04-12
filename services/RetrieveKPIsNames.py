from datetime import datetime
from services.calculations.revenueCalculation import calculateRevenue
from core.models.base.ResultModel import Result


def retriveKPIsNames():
    try:
        resultDict = {
            "PROFITIABILITY" :{
            "TotalRevenue" : calculateRevenue().Data
            }
        }

        return Result(
            Data=resultDict,
            Status=1,
            Message="KPIs Name retrieve Succesfully",
        )

    except Exception as ex:
        message = f"Error occur at retriveKPIsNames: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
