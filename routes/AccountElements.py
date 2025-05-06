from fastapi import APIRouter, Body
from services.accountNames.GetFinancialsNames import retreiveFinacialsNames
from services.accountValues.RetriveData import getValues
from services.calculations.Revenue import totalRevenue, revenueGrowth
from services.calculations.NetIncome import netIncome
from typing import Optional, List
from services.reportSection.financialHeights.tables.RevenueBreakDown import (
    getRevenueTable,
)
from services.calculations.OtherIncome import otherIncome
from core.models.base.DateFilterModel import DateFilter
from services.reportSection.expensesAnalysis.tables.TopOperatingExpenses import getTopOpeatingExpenses
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
    return getTopOpeatingExpenses(
        year=2024,
        months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        reportType="Yearly",
        section="Financial Heights")
