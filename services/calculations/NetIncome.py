from datetime import datetime
from config.variable import variableMapping
from core.models.base.ResultModel import Result
from services.calculations.Revenue import totalRevenue
from services.calculations.EarningBefore import (
    earningBeforeTax,
)

from helper.GetValueSum import getValueSum
from typing import Optional
from helper.LoadJsonData import financialDataTest
from helper.GetFileByReportId import getReportData


# Operating Profit
def netIncome(year: int, month, reportId: Optional[int] = None):
    try:
        financialData = financialDataTest

        if reportId is not None:
            financialData = getReportData(reportId)["Financial Data"]

        TEXPdata = financialData["PROFIT & LOSS"]["OTHER EXPENSES"]["Classification"][
            "Tax Expense"
        ]

        TEXPFilter = [
            item
            for item in TEXPdata
            if (item["Year"] == year and (0 in month or item["Month"] in month))
        ]

        totalTEXP = sum(item["Value"] for item in TEXPFilter)

        ebt = earningBeforeTax(year, month, reportId).Data

        result = ebt - totalTEXP

        return Result(
            Data=round(result, 2),
            Status=1,
            Message="Total netIncome calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at netIncome: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at netIncome: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)


def netIncomeMargin(year: int, month, reportId: Optional[int] = None):
    try:

        
        totalRev = totalRevenue(year, month, reportId).Data


        NIC = netIncome(year, month, reportId).Data



        netICMargin = (NIC / totalRev) * 100

        return Result(
            Data=round(netICMargin, 2),
            Status=1,
            Message="Total netIncomeMargin calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at netIncomeMargin: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at netIncomeMargin: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)


def otherIncome(year: int, months, reportId: Optional[int] = None):
    try:
        financialData = (
            getReportData(reportId)["Financial Data"] if reportId else financialDataTest
        )

        #  Income without interest
        totaltherIncome = getValueSum(
            financialData,
            ["PROFIT & LOSS", "OTHER INCOME", "Classification", "Additional Income"],
            year,
            months,
        ).Data

        return Result(
            Data=round(totaltherIncome, 2),
            Status=1,
            Message="Total netIncomeMargin calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at netIncomeMargin: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at netIncomeMargin: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
