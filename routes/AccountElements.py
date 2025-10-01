from fastapi import APIRouter, Body
from services.accountNames.GetFinancialsNames import retreiveFinacialsNames
from services.accountValues.RetriveData import getValues
from typing import Optional
from core.models.base.DateFilterModel import DateFilter
from services.ExtractDataRange import retriveDataRange
from core.models.base.ResultModel import Result
from services.calculations.CashFlowStatements import getNetCashFlow
from services.calculations.Accountablity import getAP,getAPdays,getAR,getARdays,getCOGS
from services.calculations.Ratios import cashRatio,currentRatio,workingCapital


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
    return currentRatio(
        year=2025,
        months=[8],
        reportId=76581
    )
    