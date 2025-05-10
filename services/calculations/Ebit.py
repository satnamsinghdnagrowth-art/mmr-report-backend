from datetime import datetime
from typing import Optional
from config.variable import variableMapping
from core.models.base.ResultModel import Result
from services.calculations.Revenue import totalRevenue
from services.calculations.GrossProfit import grossProfit
from services.calculations.Expenses import totalOperatingExpenses


def EBIT(year: int, month, reportId: Optional[int] = None):
    try:
        GP = grossProfit(year, month, reportId).Data

        operatingCost = totalOperatingExpenses(year, month, reportId).Data

        totalEBIT = GP - operatingCost

        return Result(
            Data=round(totalEBIT, 2),
            Status=1,
            Message="Total EBIT calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at EBIT: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at totalRevenue: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)


# Get EBIT Margin
def EBITMargin(year: int, month, reportId: Optional[int] = None):
    try:
        totalRev = totalRevenue(year, month, reportId).Data
        totalEBIT = EBIT(year, month, reportId).Data

        ebitMargin = (totalEBIT / totalRev) * 100

        return Result(
            Data=round(ebitMargin, 2),
            Status=1,
            Message="EBIT Margin calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at EBITMargin: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at totalRevenue: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
