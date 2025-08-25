from datetime import datetime
from config.variable import variableMapping
from core.models.base.ResultModel import Result
from services.calculations.Revenue import totalRevenue
from services.calculations.Expenses import directExpenses
from typing import Optional


# Get Gross Profit
def grossProfit(year: int, month, reportId: Optional[int] = None):
    try:
        totalRev = totalRevenue(year, month, reportId).Data
        grossProfit = totalRev - directExpenses(year, month, reportId).Data

        return Result(
            Data=round(grossProfit, 2),
            Status=1,
            Message="Gross Profit calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at grossProfit: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at grossProfit: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)


# Get Gross Profit Margin
def grossProfitMargin(year: int, month, reportId: Optional[int] = None):
    try:
        totalRev = totalRevenue(year, month, reportId).Data
        GP = grossProfit(year, month, reportId).Data
        GPM = (GP / totalRev) * 100

        return Result(
            Data=round(GPM, 2),
            Status=1,
            Message="Gross Profit calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at grossProfitMargin: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at totalRevenue: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
