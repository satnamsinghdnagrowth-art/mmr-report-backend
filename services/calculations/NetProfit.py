from datetime import datetime
from core.models.base.ResultModel import Result
from services.calculations.Ebit import EBIT
from services.calculations.Revenue import totalRevenue
from helper.LoadJsonData import financialDataTest
from typing import Optional
from helper.GetFileByReportId import getReportData


# Get Total Revenue
def netProfit(year: int, month, reportId: Optional[int] = None):
    try:
        financialData = financialDataTest

        if reportId is not None:
            financialData = getReportData(reportId)["Financial Data"]

        ebit = EBIT(year, month).Data

        # Interest Expenses
        IEXPdata = financialData["PROFIT & LOSS"]["OTHER EXPENSES"]["Classification"][
            "Interest Expense"
        ]

        IEXPFilter = [
            item
            for item in IEXPdata
            if (item["Year"] == year and (0 in month or item["Month"] in month))
        ]

        totalIEXP = IEXPFilter[0]["Value"] if IEXPFilter else 0

        # Tax Expenses
        TEXPdata = financialData["PROFIT & LOSS"]["OTHER EXPENSES"]["Classification"][
            "Tax Expense"
        ]

        TEXPFilter = [
            item
            for item in TEXPdata
            if (item["Year"] == year and (0 in month or item["Month"] in month))
        ]

        totalTEXP = TEXPFilter[0]["Value"] if IEXPFilter else 0

        otherExpenses = totalIEXP + totalTEXP

        netProfit = ebit - otherExpenses

        return Result(
            Data=round(netProfit, 2),
            Status=1,
            Message="NetProfit calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at netProfit: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at netProfit: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)


#  Get Total Revenue
def netProfitMargin(year: int, month, reportId: Optional[int] = None):
    try:
        netprofitValue = netProfit(year, month, reportId).Data

        totalRev = totalRevenue(year, month, reportId).Data

        netProfitMargin = (netprofitValue / totalRev) * 100

        return Result(
            Data=round(netProfitMargin, 2),
            Status=1,
            Message="NetProfit Margin calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at netProfit: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at netProfit: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
