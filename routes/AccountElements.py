from fastapi import APIRouter, Body
from services.accountNames.GetFinancialsNames import retreiveFinacialsNames
from services.accountValues.RetriveData import getValues
from services.calculations.CashFlowActivities import getOperatingActivitiesCashFlow,getInvestigatingActivitiesCashFlow
from typing import Optional, List
from services.calculations.CashFlowStatements import getFreeCashFlow
from services.reportSection.cashFlowAnalysis.charts.cashFlowChart import getEACharts
from core.models.base.DateFilterModel import DateFilter
from services.ExtractDataRange import retriveDataRange
from core.models.base.ResultModel import Result


Account = APIRouter()


# Get  Account Names
@Account.get("/get/Names")
def getAccountNames(year: int, month: int) -> Result:
    return retreiveFinacialsNames(year, month)


# Get the values for dropdown options
@Account.post("/get/data/{mainSection}/{section}")
@Account.post("/get/data/{mainSection}/{section}/{subSection}")
def get_report_values(
    mainSection: str,
    section: str,
    subSection: Optional[str] = None,
    payload: DateFilter = Body(...),
) -> Result:
    return getValues(mainSection, section, subSection, payload.Year, payload.Month)


# Get the dataRange of Report
@Account.get("/get/reportDescription")
def getReportDescription() -> Result:
    return retriveDataRange()


# Test the calulation
@Account.get("/get/Calculations")
def calculation() -> Result:
    return getFreeCashFlow(year=2024,
        months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],reportId=12345)
    # return getCashFlowTable(year=2024, tableType="bj")
    # return getCashOnHand(
    #     year=2024,
    #     months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    #     # reportType="Year",
    #     # section="Financial Heights",
    # )
