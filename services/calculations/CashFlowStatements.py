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

        print(totalInterestIncome,"cvbjvcb")

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
            getTotalCurrentAssets(year, [months[-1]]).Data
            - getTotalCurrentAssets(year - 1, [months[-1]]).Data
        )
        changeInCl = (
            getTotalCurrentLiabilities(year, [months[-1]]).Data
            - getTotalCurrentLiabilities(year - 1, [months[-1]]).Data
        )

        print(f"Tax:{totalTEXP} in CL:{changeInCl},change in CA :{changeInCa},netProfit :{netProfitTotal},DP:{totalDepreciation},interst Ee:{totalInterestExpense},tot Interrs Incomr{totalInterestIncome}")

        cashFlow =  (netProfitTotal+ totalDepreciation+ totalInterestExpense - totalInterestIncome +totalTEXP)+ (changeInCl + changeInCa)
        

        return Result(
            Data=round(cashFlow, 2),
            Status=1,
            Message="Total contribution calculated successfully",
        )

    except Exception as ex:
        message = f"Error occur at contribution: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
    

def getCashOnHand(year: int, months, reportId: Optional[int] = None):
    try:
        financialData = getReportData(reportId) if reportId else financialDataTest

        totalCash = getValueSum(
            financialData,
            ["BalanceSheet", "CURRENT ASSETS", "Classification", "Cash"],
            year,
            [months[-1]],
        ).Data



        return Result(
            Data=round(totalCash, 2),
            Status=1,
            Message="Total contribution calculated successfully",
        )

    except Exception as ex:
        message = f"Error occur at contribution: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)

