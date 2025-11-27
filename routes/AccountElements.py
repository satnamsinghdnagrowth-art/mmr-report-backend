from fastapi import APIRouter, Body
from services.accountNames.GetFinancialsNames import retreiveFinacialsNames
from services.accountValues.RetriveData import getValues
from typing import Optional
from core.models.base.DateFilterModel import DateFilter
from services.ExtractDataRange import retriveDataRange
from core.models.base.ResultModel import Result
from services.calculations.Revenue import totalRevenue
from core.models.base.SourceModel import SourceDataTypes
from core.models.base.ColorModel import ColorsModel
from services.budget.VarianceAnalysisTable import varianceTable

AccountItemsRouter = APIRouter()

# Get  Account Names
@AccountItemsRouter.get("/get/Names/report/{reportId}", response_model=Result)
def getAccountNames(year: int, month: int, reportId: int) -> Result:
    return retreiveFinacialsNames(year, month, reportId)


# Get the values for dropdown options
@AccountItemsRouter.post(
    "/get/data/report/{reportId}/{mainSection}/{section}", response_model=Result
)
@AccountItemsRouter.post(
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
@AccountItemsRouter.get("/get/reportDescription", response_model=Result)
def getReportDescription():
    return retriveDataRange()


# Test the calulation
@AccountItemsRouter.get("/get/Calculations")
def calculation() -> Result:
    return varianceTable(
        year=2025, month=[9], reportId=24639, dataType=SourceDataTypes.Actuals
    )
