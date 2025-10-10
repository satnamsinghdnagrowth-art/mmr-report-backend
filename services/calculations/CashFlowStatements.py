from datetime import datetime
from core.models.base.ResultModel import Result
from helper.LoadJsonData import financialDataTest
from typing import Optional
from helper.GetFileByReportId import getReportData
from services.calculations.CashFlowActivities import (
    getInvestigatingActivitiesCashFlow,
    getOperatingActivitiesCashFlow,
    getFinancingActivitiesCashFlow,
)
from helper.GetValueSum import getValueSum


def getFreeCashFlow(year: int, months, reportId: Optional[int] = None):
    try:
        freeCashFlow = (
            getOperatingActivitiesCashFlow(year, months, reportId).Data
            + getInvestigatingActivitiesCashFlow(year, months, reportId).Data
        )

        return Result(
            Data=round(freeCashFlow, 2),
            Status=1,
            Message="Total FreeCashFlow calculated successfully",
        )

    except Exception as ex:
        message = f"Error occur at FreeCashFlow: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)


def getCashOnHand(year: int, months, reportId: Optional[int] = None):
    try:
        financialData = (
            getReportData(reportId)["Financial Data"] if reportId else financialDataTest
        )

        totalCash = getValueSum(
            financialData,
            ["BalanceSheet", "CURRENT ASSETS", "Classification", "Cash & Equivalents"],
            year,
            [months[-1]],
        ).Data

        return Result(
            Data=round(totalCash, 2),
            Status=1,
            Message="Total CashOnHand calculated successfully",
        )

    except Exception as ex:
        message = f"Error occur at CashOnHand: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)


def getNetCashFlow(year: int, months, reportId: Optional[int] = None):
    try:
        netCashFlow = (
            getOperatingActivitiesCashFlow(year, months, reportId).Data
            + getInvestigatingActivitiesCashFlow(year, months, reportId).Data
            + getFinancingActivitiesCashFlow(year, months, reportId).Data
        )

        return Result(
            Data=round(netCashFlow, 2),
            Status=1,
            Message="Total NetCashFlow calculated successfully",
        )

    except Exception as ex:
        message = f"Error occur at contribution: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
