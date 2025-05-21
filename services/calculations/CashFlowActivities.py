from datetime import datetime
from core.models.base.ResultModel import Result
from services.calculations.Ebit import EBIT
from services.calculations.Revenue import totalRevenue
from helper.LoadJsonData import financialDataTest
from typing import Optional
from helper.GetFileByReportId import getReportData
from services.calculations.NetIncome import netIncome
from services.calculations.CurrentAssestAndLiabilities import (
    getTotalCurrentLiabilities,
    getTotalCurrentAssets,
)
from services.calculations.NetProfit import netProfit
from helper.GetValueSum import getValueSum


# Operating Profit
def getOperatingActivitiesCashFlow(year: int, months, reportId: Optional[int] = None):
    try:
        financialData = getReportData(reportId) if reportId else financialDataTest

        totalInterestIncome = getValueSum(
            financialData,
            ["PROFIT & LOSS", "OTHER INCOME", "Classification", "Interest Income"],
            year,
            months,
        ).Data

        totalDepreciation = getValueSum(
            financialData,
            ["PROFIT & LOSS", "EXPENSES", "Classification", "Depreciation"],
            year,
            months,
        ).Data

        totalInterestExpense = getValueSum(
            financialData,
            ["PROFIT & LOSS", "OTHER EXPENSES", "Classification", "Interest Expense"],
            year,
            months,
        ).Data

        TEXPdata = financialData["PROFIT & LOSS"]["OTHER EXPENSES"]["Classification"][
            "Tax Expense"
        ]

        TEXPFilter = [
            item
            for item in TEXPdata
            if (item["Year"] == year and (0 in months or item["Month"] in months))
        ]

        totalTEXP = sum(item["Value"] for item in TEXPFilter)

        netProfitTotal = netIncome(year, months, reportId).Data
        changeInCa = (
            getTotalCurrentAssets(year - 1, [months[-1]]).Data
            - getTotalCurrentAssets(year, [months[-1]]).Data
        )
        changeInCl = (
            getTotalCurrentLiabilities(year, [months[-1]]).Data
            - getTotalCurrentLiabilities(year - 1, [months[-1]]).Data
        )

        netIncomeAfterAdjustment = (
            netProfitTotal
            + totalDepreciation
            + totalInterestExpense
            - totalInterestIncome
        )

        operatingActivitesCashFlow = netIncomeAfterAdjustment + changeInCl + changeInCa

        return Result(
            Data=round(operatingActivitesCashFlow, 2),
            Status=1,
            Message="Total operatingActivitesCashFlow calculated successfully",
        )

    except Exception as ex:
        message = f"Error occur at getOperatingActivitiesCashFlow: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)


def getInvestigatingActivitiesCashFlow(
    year: int, months, reportId: Optional[int] = None
):
    try:
        financialData = getReportData(reportId) if reportId else financialDataTest

        changeInFA = (
            getValueSum(
                financialData,
                [
                    "BalanceSheet",
                    "NON-CURRENT ASSETS",
                    "Classification",
                    "Fixed Assets",
                ],
                year - 1,
                [months[-1]],
            ).Data
            - getValueSum(
                financialData,
                [
                    "BalanceSheet",
                    "NON-CURRENT ASSETS",
                    "Classification",
                    "Fixed Assets",
                ],
                year,
                [months[-1]],
            ).Data
        )

        changeInIA = (
            getValueSum(
                financialData,
                [
                    "BalanceSheet",
                    "NON-CURRENT ASSETS",
                    "Classification",
                    "Intangible Assets",
                ],
                year - 1,
                [months[-1]],
            ).Data
            - getValueSum(
                financialData,
                [
                    "BalanceSheet",
                    "NON-CURRENT ASSETS",
                    "Classification",
                    "Intangible Assets",
                ],
                year,
                [months[-1]],
            ).Data
        )

        changeInONCA = (
            getValueSum(
                financialData,
                [
                    "BalanceSheet",
                    "NON-CURRENT ASSETS",
                    "Classification",
                    "Other Non-Current Assets",
                ],
                year - 1,
                [months[-1]],
            ).Data
            - getValueSum(
                financialData,
                [
                    "BalanceSheet",
                    "NON-CURRENT ASSETS",
                    "Classification",
                    "Other Non-Current Assets",
                ],
                year,
                [months[-1]],
            ).Data
        )

        totalInterestExpense = getValueSum(
            financialData,
            ["PROFIT & LOSS", "OTHER INCOME", "Classification", "Interest Income"],
            year,
            months,
        ).Data

        investigatingActivitiesCashFlow = (
            changeInFA + changeInIA + changeInONCA + totalInterestExpense
        )

        return Result(
            Data=round(investigatingActivitiesCashFlow, 2),
            Status=1,
            Message="Total operatingActivitesCashFlow calculated successfully",
        )

    except Exception as ex:
        message = f"Error occur at getInvestigatingActivitiesCashFlow: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
