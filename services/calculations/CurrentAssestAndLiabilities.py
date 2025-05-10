from datetime import datetime
from core.models.base.ResultModel import Result
from services.calculations.Ebit import EBIT
from services.calculations.Revenue import totalRevenue
from helper.LoadJsonData import financialDataTest
from helper.GetFileByReportId import getReportData
from typing import Optional


# Operating Profit
def getTotalCurrentLiabilities(year: int, months, reportId: Optional[int] = None):
    try:
        financialData = financialDataTest

        if reportId is not None:
            financialData = getReportData(reportId)

        STDdata = financialDataTest["BalanceSheet"]["CURRENT LIABILITIES"][
            "Classification"
        ]["Short-term Debt"]

        STDFilter = [
            item
            for item in STDdata
            if (item["Year"] == year and (0 in months or item["Month"] in months))
        ]

        totalSTD = sum(item["Value"] for item in STDFilter)

        APdata = financialDataTest["BalanceSheet"]["CURRENT LIABILITIES"][
            "Classification"
        ]["Accounts Payable"]

        APFilter = [
            item
            for item in APdata
            if (item["Year"] == year and (0 in months or item["Month"] in months))
        ]

        totalAP = sum(item["Value"] for item in APFilter)

        TLdata = financialDataTest["BalanceSheet"]["CURRENT LIABILITIES"][
            "Classification"
        ]["Taxes & Levies"]

        TLFilter = [
            item
            for item in TLdata
            if (item["Year"] == year and (0 in months or item["Month"] in months))
        ]

        totalTL = sum(item["Value"] for item in TLFilter)

        OCLdata = financialDataTest["BalanceSheet"]["CURRENT LIABILITIES"][
            "Classification"
        ]["Other Current Liabilities"]

        OCLFilter = [
            item
            for item in OCLdata
            if (item["Year"] == year and (0 in months or item["Month"] in months))
        ]

        totalOCL = sum(item["Value"] for item in OCLFilter)

        totalCL = totalSTD + totalAP + totalTL + totalOCL

        return Result(
            Data=round(totalCL, 2),
            Status=1,
            Message="Total contribution calculated successfully",
        )

    except Exception as ex:
        message = f"Error occur at contribution: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)


def getTotalCurrentAssets(year: int, months, reportId: Optional[int] = None):
    try:
        ARdata = financialDataTest["BalanceSheet"]["CURRENT ASSETS"]["Classification"][
            "Accounts Receivable"
        ]

        ARFilter = [
            item
            for item in ARdata
            if (item["Year"] == year and (0 in months or item["Month"] in months))
        ]

        totalAR = sum(item["Value"] for item in ARFilter)

        INVdata = financialDataTest["BalanceSheet"]["CURRENT ASSETS"]["Classification"][
            "Inventory"
        ]

        INVFilter = [
            item
            for item in INVdata
            if (item["Year"] == year and (0 in months or item["Month"] in months))
        ]

        totalINV = sum(item["Value"] for item in INVFilter)

        WIPdata = financialDataTest["BalanceSheet"]["CURRENT ASSETS"]["Classification"][
            "Work In Progress"
        ]

        WIPFilter = [
            item
            for item in WIPdata
            if (item["Year"] == year and (0 in months or item["Month"] in months))
        ]

        totalWIP = sum(item["Value"] for item in WIPFilter)

        OCAdata = financialDataTest["BalanceSheet"]["CURRENT ASSETS"]["Classification"][
            "Other Current Assets"
        ]

        OCAFilter = [
            item
            for item in OCAdata
            if (item["Year"] == year and (0 in months or item["Month"] in months))
        ]

        totalOCA = sum(item["Value"] for item in OCAFilter)

        print(totalAR,totalINV,totalOCA,"Balance Sheet")


        totalCA = totalAR + totalOCA + totalINV 
        print(year,totalCA,months,"curren Assets")

        return Result(
            Data=round(totalCA, 2),
            Status=1,
            Message="Total contribution calculated successfully",
        )

    except Exception as ex:
        message = f"Error occur at getTotalCurrentAssets: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
