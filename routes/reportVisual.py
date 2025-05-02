from fastapi import APIRouter
from core.models.base.ResultModel import Result
from services.reportSection.financialHeights.SectionData import getSectionData
from services.reportSection.financialHeights.cardsKPIs import getSectionCards
from services.reportSection.financialHeights.chartsKPIs import getSectionCharts
from core.models.base.SectionDataRequestBody import SectionChartRequestData
from services.reportSection.financialHeights.tables.IncomeStatementTablesKPI import (
    getISTable,
)

visual = APIRouter()

# for testing
year = (2024,)
months = ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],)
reportType = ("Yearly",)
section = ("Financial Heights",)


# Get Financial Higlights Section All Data
@visual.get("/get/financialHeights/")
def getCards()->Result:
    return getSectionData(
        year=2024,
        months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        reportType="Yearly",
        section="Financial Heights",
    )


# Get Financial Higlights Section Cards
@visual.post("/get/financialHeights/cards")
def getCards(payload: SectionChartRequestData)-> Result:
    return getSectionCards(
        year=payload.Year,
        months=payload.Months,
        reportType=payload.ReportType,
        section=payload.SectionName,
    )


# Get Financial Higlights Section Charts
@visual.post("/get/financialHeights/charts")
def getCards(payload: SectionChartRequestData) -> Result:
    return getSectionCharts(
        year=payload.Year,
        months=payload.Months,
        reportType=payload.ReportType,
        section=payload.SectionName,
    )


# Get Financial Higlights Section Tables
@visual.post("/get/financialHeights/tables")
def getTables(payload: SectionChartRequestData) -> Result:
    return getISTable(
        year=payload.Year,
        months=payload.Months,
        reportType=payload.ReportType,
        section=payload.SectionName,
    )
