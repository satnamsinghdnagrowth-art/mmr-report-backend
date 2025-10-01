from datetime import datetime
from core.models.base.ResultModel import Result
from services.calculations.Revenue import totalRevenue
from helper.LoadJsonData import financialDataTest
from typing import Optional,List
from helper.GetFileByReportId import getReportData
from services.calculations.COGS import getCOGS
from services.calculations.CurrentAssestAndLiabilities import getTotalCurrentAssets , getTotalCurrentLiabilities

# Current Ratio
def currentRatio(year: int, months:List[int], reportId: Optional[int] = None):
    try:
        financialData = (
            getReportData(reportId)["Financial Data"] if reportId else financialDataTest
        )

        CASHdata = financialData["BalanceSheet"]["CURRENT ASSETS"]["Classification"][
            "Cash & Equivalents"
        ]

        CASHFilter = [
            item
            for item in CASHdata
            if (item["Year"] == year and (0 in months or item["Month"] in months))
        ]

        totalCASH = sum(item["Value"] for item in CASHFilter)   

        totalCA = getTotalCurrentAssets(year, months, reportId).Data
        totalCL = getTotalCurrentLiabilities(year, months, reportId).Data

        totalCurrentRatio = (totalCA + totalCASH) / totalCL

        return Result(
            Data=round(totalCurrentRatio, 2),
            Status=1,
            Message="Total currentRatio calculated successfully",
        )

    except Exception as ex:
        message = f"Error occur at currentRatio: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
    
# Cash Ratio
def cashRatio(year: int, months:List[int], reportId: Optional[int] = None):
    try:

        totalCL = getTotalCurrentLiabilities(year, months, reportId).Data 

        financialData = (
            getReportData(reportId)["Financial Data"] if reportId else financialDataTest
        )

        cashData = financialData["BalanceSheet"]["CURRENT ASSETS"]["Classification"][
            "Cash & Equivalents"
        ]

        cashFilter = [
            item
            for item in cashData
            if (item["Year"] == year and (0 in months or item["Month"] in months))
        ]

        totalCash = sum(item["Value"] for item in cashFilter)

        totalCashRation = totalCash / totalCL

        return Result(
            Data=round(totalCashRation, 2),
            Status=1,
            Message="Total Cash Ratio calculated successfully",
        )

    except Exception as ex:
        message = f"Error occur at cashRatio: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
    
# Working Capital 
def workingCapital(year: int, months:List[int], reportId: Optional[int] = None):
    try:
        financialData = (
            getReportData(reportId)["Financial Data"] if reportId else financialDataTest
        )

        CASHdata = financialData["BalanceSheet"]["CURRENT ASSETS"]["Classification"][
            "Cash & Equivalents"
        ]

        CASHFilter = [
            item
            for item in CASHdata
            if (item["Year"] == year and (0 in months or item["Month"] in months))
        ]

        totalCASH = sum(item["Value"] for item in CASHFilter)

        totalCA = getTotalCurrentAssets(year, months, reportId).Data

        totalCL = getTotalCurrentLiabilities(year, months, reportId).Data

        totalWorkingCapital = (totalCA + totalCASH) - totalCL

        return Result(
            Data=round(totalWorkingCapital, 2),
            Status=1,
            Message="Total workingCapital calculated successfully",
        )

    except Exception as ex:
        message = f"Error occur at workingCapital: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)