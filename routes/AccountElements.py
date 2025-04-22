from fastapi import APIRouter
from services.GetFinancialsNames import retreiveFinacialsNames
from services.GetFinancialsValues import retreiveFinacialsValues
from services.retriveData import getDataValues,getTestValues
from services.ExtractDataRange import retriveDataRange
from core.models.base.ResultModel import Result

Account = APIRouter()

# Get  Account Names
@Account.get("/get/Names")
def getAccountNames( 
    year: int = None,
    month: int = None) -> Result:
    return retreiveFinacialsNames(year,month)


# Get  Account Values
@Account.get("/get/Values")
def getReportValues() -> Result:
    return retreiveFinacialsValues()

# Get  Account Values
@Account.get("/get/data/{mainSection}/{section}/{sub_section}")
def get_report_values(
    mainSection: str,
    section: str,
    sub_section: str,
    year: int = None,
    month: int = None
) -> Result:
    return getTestValues(mainSection, section, sub_section, year, month)


@Account.get("/get/reportDescription")
def getReportDescription() -> Result:
    return retriveDataRange()
