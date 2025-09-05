from datetime import datetime
from typing import Optional
from config.variable import variableMapping
from core.models.base.ResultModel import Result
from services.calculations.Revenue import totalRevenue
from services.calculations.GrossProfit import  operatingProfit
from helper.GetValueSum import getValueSum
from typing import Optional
from helper.LoadJsonData import financialDataTest
from helper.GetFileByReportId import getReportData


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
    
def otherExpenses(year: int, months, reportId: Optional[int] = None):
    try:
        financialData = (
            getReportData(reportId)["Financial Data"] if reportId else financialDataTest
        )

        #  Income without interest
        totaltherIncome = getValueSum(
            financialData,
            ["PROFIT & LOSS", "OTHER EXPENSES", "Classification", "Other Expenses"],
            year,
            months,
        ).Data

        return Result(
            Data=round(totaltherIncome, 2),
            Status=1,
            Message="Total otherExpenses calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at netIncomeMargin: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at netIncomeMargin: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)


def EBIT(year: int, month, reportId: Optional[int] = None):
    try:
        # GP = grossProfit(year, month, reportId).Data

        # operatingCost = totalOperatingExpenses(year, month, reportId).Data

        # totalEBIT = GP - operatingCost

        opertaingProfitValue = operatingProfit(year, month, reportId).Data

        otherIncomeValue = otherIncome(year, month, reportId).Data

        otherExpensesValue = otherExpenses(year, month, reportId).Data
        
        result = opertaingProfitValue + otherIncomeValue - otherExpensesValue

        return Result(
            Data=round(result, 2),
            Status=1,
            Message="Total EBIT calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at EBIT: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at totalRevenue: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)


# Get EBIT Margin
def EBITMargin(year: int, month, reportId: Optional[int] = None):
    try:
        totalRev = totalRevenue(year, month, reportId).Data
        totalEBIT = EBIT(year, month, reportId).Data

        ebitMargin = (totalEBIT / totalRev) * 100

        return Result(
            Data=round(ebitMargin, 2),
            Status=1,
            Message="EBIT Margin calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at EBITMargin: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at totalRevenue: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
