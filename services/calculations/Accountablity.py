from datetime import datetime
from core.models.base.ResultModel import Result
from services.calculations.Revenue import totalRevenue
from helper.LoadJsonData import financialDataTest
from typing import Optional,List
from helper.GetFileByReportId import getReportData
from services.calculations.COGS import getCOGS

# Account Receivables
def getAR(year: int, months:List[int], reportId: Optional[int] = None):
    try:
        financialData = (
            getReportData(reportId)["Financial Data"] if reportId else financialDataTest
        )

        ARdata = financialData["BalanceSheet"]["CURRENT ASSETS"]["Classification"][
            "Accounts Receivable"
        ]

        ARFilter = [
            item
            for item in ARdata
            if (item["Year"] == year and (0 in months or item["Month"] in months))
        ]

        totalAR = sum(item["Value"] for item in ARFilter)

    
        return Result(
            Data=round(totalAR, 2),
            Status=1,
            Message="Total getAP calculated successfully",
        )

    except Exception as ex:
        message = f"Error occur at getAR: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
    

# Account Payables
def getAP(year: int, months:List[int], reportId: Optional[int] = None):
    try:
        financialData = (
            getReportData(reportId)["Financial Data"] if reportId else financialDataTest
        )

        APdata = financialData["BalanceSheet"]["CURRENT LIABILITIES"]["Classification"][
            "Accounts Payable"
        ]

        APFilter = [
            item
            for item in APdata
            if (item["Year"] == year and (0 in months or item["Month"] in months))
        ]

        totalAP = sum(item["Value"] for item in APFilter)

        return Result(
            Data=round(totalAP, 2),
            Status=1,
            Message="Total getAP calculated successfully",
        )

    except Exception as ex:
        message = f"Error occur at getAP: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
    
# Account Payables Days
def getAPdays(year: int, months:List[int], reportId: Optional[int] = None):
    try:
        print(year)
        totalAP = getAP(year,months,reportId).Data

        totalCOG = getCOGS(year,months,reportId).Data

        AP_Days = (totalAP /totalCOG) * 365

        return Result(
            Data=round(AP_Days, 2),
            Status=1,
            Message="Total getAPdays calculated successfully",
        )

    except Exception as ex:
        message = f"Error occur at getAPdays: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
    
    
def getARdays(year: int, months:List[int], reportId: Optional[int] = None):
    try:

        totalRev = totalRevenue(year,months, reportId).Data

        totalAR = getAR(year,months,reportId).Data

        AR_Days = (totalAR/totalRev) * 365

        return Result(
            Data=AR_Days,
            Status=1,
            Message="Total getARdays calculated successfully",
        )

    except Exception as ex:
        message = f"Error occur at getARdays: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
    