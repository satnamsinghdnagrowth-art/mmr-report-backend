from datetime import datetime
from core.models.base.ResultModel import Result
from services.calculations.Revenue import totalRevenue
from helper.LoadJsonData import financialDataTest
from typing import Optional, List
from helper.GetFileByReportId import getReportData


# Account Receivables
def getCOGS(year: int, months: List[int], reportId: Optional[int] = None):
    try:
        financialData = (
            getReportData(reportId)["Financial Data"] if reportId else financialDataTest
        )

        FCOSdata = financialData["BalanceSheet"]["CURRENT ASSETS"]["Classification"][
            "Accounts Receivable"
        ]

        FCOSFilter = [
            item
            for item in FCOSdata
            if (item["Year"] == year and (0 in months or item["Month"] in months))
        ]

        totalFCOS = sum(item["Value"] for item in FCOSFilter)

        VCOSdata = financialData["BalanceSheet"]["CURRENT ASSETS"]["Classification"][
            "Accounts Receivable"
        ]

        VCOSFilter = [
            item
            for item in VCOSdata
            if (item["Year"] == year and (0 in months or item["Month"] in months))
        ]

        totalVCOS = sum(item["Value"] for item in VCOSFilter)

        totalCOGS = totalFCOS + totalVCOS

        return Result(
            Data=round(totalCOGS, 2),
            Status=1,
            Message="Total getCOGS calculated successfully",
        )

    except Exception as ex:
        message = f"Error occur at getCOGS: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
