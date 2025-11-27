from datetime import datetime
from core.models.base.ResultModel import Result
from helper.LoadJsonData import financialDataTest
from typing import Optional, List
from helper.GetFileByReportId import getReportData
from services.calculations.NetIncome import netIncome
from services.calculations.CurrentAssestAndLiabilities import (
    getTotalCurrentLiabilities,
    getTotalCurrentAssets,
)
from core.models.base.SourceModel import SourceDataTypes
from helper.GetCurrentPrevPeriods import getCurrentAndPreviousPeriods
from helper.GetValueSum import getValueSum
from helper.GetFinancialData import getFinancialData



# Operating Profit
def getOperatingActivitiesCashFlow(year: int,months: List[int], reportId: int,dataType: Optional[str] = SourceDataTypes.Actuals):
    try:
        if len(months) == 1:
            reportType = "Month"
        else:
            reportType = "Year"

        financialData = getFinancialData(reportId, dataType)
        
        totalInterestIncome = getValueSum(
            financialData,
            ["PROFIT & LOSS", "INTEREST INCOME", "Classification", "Interest Income"],
            year,
            months,
        ).Data

        totalDepreciation = getValueSum(
            financialData,
            ["PROFIT & LOSS", "EXPENSES", "Classification", "Depreciation"],
            year,
            months,
        ).Data

        totalDA = getValueSum(
            financialData,
            ["PROFIT & LOSS", "COST OF SALES", "Classification", "Depreciation"],
            year,
            months,
        ).Data

        totalInterestExpense = getValueSum(
            financialData,
            [
                "PROFIT & LOSS",
                "INTEREST EXPENSES",
                "Classification",
                "Interest Expense",
            ],
            year,
            months,
        ).Data

        TEXPdata = financialData["PROFIT & LOSS"]["TAX EXPENSES"]["Classification"][
            "Tax Expense"
        ]

        TEXPFilter = [
            item
            for item in TEXPdata
            if (item["Year"] == year and (0 in months or item["Month"] in months))
        ]

        totalTEXP = sum(item["Value"] for item in TEXPFilter)

        netProfitTotal = netIncome(year, months, reportId).Data
        if reportType.lower() == "year":
            changeInCa = (
                getTotalCurrentAssets(year - 1, [months[-1]], reportId).Data
                - getTotalCurrentAssets(year, [months[-1]], reportId).Data
            )

            changeInCl = (
                getTotalCurrentLiabilities(year, [months[-1]], reportId).Data
                - getTotalCurrentLiabilities(year - 1, [months[-1]], reportId).Data
            )

        else:
            changeInCa = (
                getTotalCurrentAssets(year, [months[-1] - 1], reportId).Data
                - getTotalCurrentAssets(year, [months[-1]], reportId).Data
            )

            changeInCl = (
                getTotalCurrentLiabilities(year, [months[-1]], reportId).Data
                - getTotalCurrentLiabilities(year, [months[-1] - 1], reportId).Data
            )

        # netIncomeAfterAdjustment = (
        #     netProfitTotal
        #     + totalDepreciation
        #     + totalInterestExpense
        #     - totalInterestIncome
        # )

        netIncomeValue = netIncome(year, months, reportId).Data

        operatingActivitesCashFlow = (
            netIncomeValue + changeInCl + changeInCa + totalDepreciation + totalDA
        )

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
    year: int,months: List[int], reportId: int,dataType: Optional[str] = SourceDataTypes.Actuals
):
    try:
        financialData = getFinancialData(reportId, dataType)
        changeInFA = (
            getValueSum(
                financialData,
                [
                    "BalanceSheet",
                    "NON-CURRENT ASSETS",
                    "Classification",
                    "Fixed Assets",
                ],
                year,
                [months[-1] - 1],
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

        totalDepreciation = getValueSum(
            financialData,
            ["PROFIT & LOSS", "EXPENSES", "Classification", "Depreciation"],
            year,
            months,
        ).Data

        totalDA = getValueSum(
            financialData,
            ["PROFIT & LOSS", "COST OF SALES", "Classification", "Depreciation"],
            year,
            months,
        ).Data

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
                year,
                [months[-1] - 1],
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
            ["PROFIT & LOSS", "INTEREST INCOME", "Classification", "Interest Income"],
            year,
            months,
        ).Data

        investigatingActivitiesCashFlow = (
            changeInIA + changeInONCA + (changeInFA - (totalDepreciation + totalDA))
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


def getFinancingActivitiesCashFlow(
    year: int,months: List[int], reportId: int,dataType: Optional[str] = SourceDataTypes.Actuals
):
    try:
        financialData = getFinancialData(reportId, dataType)
        currentYear, currentMonths, prevYear, prevMonths = getCurrentAndPreviousPeriods(
            year, [months[-1]], "month"
        )

        chaneInOEQ = (
            getValueSum(
                financialData,
                [
                    "EQUITY",
                    "EQUITY",
                    "Classification",
                    "Other Equity",
                ],
                currentYear,
                currentMonths,
            ).Data
            - getValueSum(
                financialData,
                [
                    "EQUITY",
                    "EQUITY",
                    "Classification",
                    "Other Equity",
                ],
                prevYear,
                prevMonths,
            ).Data
        )

        chaneInRE = (
            getValueSum(
                financialData,
                [
                    "EQUITY",
                    "EQUITY",
                    "Classification",
                    "Retained Earnings",
                ],
                currentYear,
                currentMonths,
            ).Data
            - getValueSum(
                financialData,
                [
                    "EQUITY",
                    "EQUITY",
                    "Classification",
                    "Retained Earnings",
                ],
                prevYear,
                prevMonths,
            ).Data
        )

        netinc = getValueSum(
            financialData,
            [
                "EQUITY",
                "EQUITY",
                "Classification",
                "Current Earnings",
            ],
            prevYear,
            prevMonths,
        ).Data

        if months[0] == 1:
            netIncomeValue = netinc
        else:
            netIncomeValue = 0

        result = chaneInOEQ + (chaneInRE - netIncomeValue)

        return Result(
            Data=round(result, 2),
            Status=1,
            Message="Total financingActivitiesCashFlow calculated successfully",
        )

    except Exception as ex:
        message = f"Error occur at getInvestigatingActivitiesCashFlow: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
