from datetime import datetime
from core.models.base.ResultModel import Result
from services.calculations.Ebit import EBIT
from services.calculations.Revenue import totalRevenue
from helper.LoadJsonData import financialDataTest


# Operating Profit
def getTotalCurrentLiabilities(year: int, month):
    try:
        totalRev = totalRevenue(year, month).Data

        VCOSdata = financialDataTest["PROFIT & LOSS"]["COST OF SALES"][
            "Classification"
        ]["Variable Cost"]

        VCOSFilter = [
            item
            for item in VCOSdata
            if (item["Year"] == year and (0 in month or item["Month"] in month))
        ]

        totalVCOS = sum(item["Value"] for item in VCOSFilter)

        VEXPdata = financialDataTest["PROFIT & LOSS"]["EXPENSES"]["Classification"][
            "Fixed Expenses"
        ]

        VEXPFilter = [
            item
            for item in VEXPdata
            if (item["Year"] == year and (0 in month or item["Month"] in month))
        ]

        totalVEXP = sum(item["Value"] for item in VEXPFilter)

        totalContribution = totalRev - totalVCOS - totalVEXP

        return Result(
            Data=round(totalContribution, 2),
            Status=1,
            Message="Total contribution calculated successfully",
        )

    except Exception as ex:
        message = f"Error occur at contribution: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)


def contributionMargin(year: int, month):
    try:
        totalContribution = contribution(year, month).Data

        totalRev = totalRevenue(year, month).Data

        totalContributionMargin = (totalContribution / totalRev) * 100
        
        return Result(
            Data=round(totalContributionMargin, 2),
            Status=1,
            Message="Total contributionMargin calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at contributionMargin: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at contributionMargin: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)