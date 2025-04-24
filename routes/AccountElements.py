from fastapi import APIRouter, Body
from services.GetFinancialsNames import retreiveFinacialsNames
from services.retriveData import getValues
from typing import Optional, List
from services.calculations.RevenueCalculation import grossProfitMargin
from core.models.base.DateFilterModel import DateFilter
from services.ExtractDataRange import retriveDataRange
from core.models.base.ResultModel import Result

Account = APIRouter()

# Get  Account Names
@Account.get("/get/Names")
def getAccountNames(year: int = None, month: int = None) -> Result:
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
    return grossProfitMargin(month=1, year=2022)
