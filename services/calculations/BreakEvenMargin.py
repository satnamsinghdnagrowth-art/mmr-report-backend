from datetime import datetime
from core.models.base.ResultModel import Result
from services.calculations.Revenue import totalRevenue
from services.calculations.Contribution import contribution, contributionMargin
from helper.LoadJsonData import financialDataTest
from typing import Optional

from helper.GetFileByReportId import getReportData


# Break Even
def breakEven(year: int, months, reportId: Optional[int] = None):
    try:
        financialData = getReportData(reportId)["Financial Data"] if reportId else financialDataTest
        
        FEXPdata = financialData["PROFIT & LOSS"]["EXPENSES"]["Classification"][
            "Fixed Expenses"
        ]

        FEXPFilter = [
            item
            for item in FEXPdata
            if (item["Year"] == year and (0 in months or item["Month"] in months))
        ]

        totalFEXP = sum(item["Value"] for item in FEXPFilter)

        FCOSdata = financialData["PROFIT & LOSS"]["COST OF SALES"][
            "Classification"
        ]["Fixed Cost"]

        FCOSFilter = [
            item
            for item in FCOSdata
            if (item["Year"] == year and (0 in months or item["Month"] in months))
        ]

        totalFCOS = sum(item["Value"] for item in FCOSFilter)


        breakEvenPoint = (
            (totalFEXP + totalFCOS) / contributionMargin(year, months,reportId).Data
        ) * 100


        return Result(
            Data=round(breakEvenPoint, 2),
            Status=1,
            Message="Total breakEven calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at breakEven: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at breakEven: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)


def breakEvenMarginSafety(year: int, months, reportId: Optional[int] = None):
    try:
        breakEvenValue = breakEven(year, months,reportId).Data

        totalRev = totalRevenue(year, months,reportId).Data

        BEMarginSafety = totalRev - breakEvenValue

        return Result(
            Data=round(BEMarginSafety, 2),
            Status=1,
            Message="Total breakEven calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at breakEven: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at breakEven: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
