from fastapi import APIRouter, Body
from services.accountNames.GetFinancialsNames import retreiveFinacialsNames
from services.accountValues.RetriveData import getValues
from typing import Optional
from services.reportSection.cashFlowAnalysis.charts.cashFlowChart import getEACharts
from core.models.base.DateFilterModel import DateFilter
from services.ExtractDataRange import retriveDataRange
from core.models.base.ResultModel import Result
from services.calculations.CashFlowActivities import  getFinancingActivitiesCashFlow

from services.calculations.CashFlowStatements import getCashOnHand, getFreeCashFlow,getNetCashFlow
Account = APIRouter()


# Get  Account Names
@Account.get("/get/Names/report/{reportId}", response_model=Result)
def getAccountNames(year: int, month: int, reportId: int) -> Result:
    return retreiveFinacialsNames(year, month, reportId)


# Get the values for dropdown options
@Account.post(
    "/get/data/report/{reportId}/{mainSection}/{section}", response_model=Result
)
@Account.post(
    "/get/data/report/{reportId}/{mainSection}/{section}/{subSection}",
    response_model=Result,
)
def get_report_values(
    mainSection: str,
    section: str,
    reportId: int,
    subSection: Optional[str] = None,
    payload: DateFilter = Body(...),
):
    return getValues(
        mainSection, section, reportId, subSection, payload.Year, payload.Month
    )



# Get the dataRange of Report
@Account.get("/get/reportDescription", response_model=Result)
def getReportDescription():
    return retriveDataRange()


# Test the calulation
@Account.get("/get/Calculations")
def calculation() -> Result:
    return getNetCashFlow(
        year=2024,
        months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        reportId=92161
    )
    