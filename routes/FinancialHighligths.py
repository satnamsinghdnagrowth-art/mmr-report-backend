from fastapi import APIRouter
from core.models.base.ResultModel import Result
from services.reportSection.financialHighlights.sectionData.SectionData import (
    getSectionData,
)
from services.reportSection.financialHighlights.cards.cardsKPIs import getSectionCards
from services.reportSection.financialHighlights.charts.chartsKPIs import (
    getSectionCharts,
)
from core.models.base.SectionDataRequestBody import SectionChartRequestData
from services.reportSection.financialHighlights.tables.IncomeStatementTablesKPI import (
    getISTable,
)

FinancialHighlights = APIRouter()

# for testing
year = 2024
months = ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],)
reportType = ("Year",)
section = "Financial Heights"



@FinancialHighlights.post("/get/sectionData/")
def getSection(payload: SectionChartRequestData) -> Result:
    return getSectionData(
        year=payload.Year,
        months=payload.Months,
        reportType=payload.ReportType,
        section=payload.SectionName,
    )

# Get Financial Higlights Section All Data
@FinancialHighlights.post("/get/sectionData/")
def getSection(payload: SectionChartRequestData) -> Result:
    return getSectionData(
        year=payload.Year,
        months=payload.Months,
        reportType=payload.ReportType,
        section=payload.SectionName,
    )


# Get Financial Higlights Section Cards
@FinancialHighlights.post("/get/financialHeights/cards")
def getCards(payload: SectionChartRequestData) -> Result:
    return getSectionCards(
        year=payload.Year,
        months=payload.Months,
        reportType=payload.ReportType,
        section=payload.SectionName,
    )


# Get Financial Higlights Section Charts
@FinancialHighlights.post("/get/financialHeights/charts")
def getCards(payload: SectionChartRequestData) -> Result:
    return getSectionCharts(
        year=payload.Year,
        months=payload.Months,
        reportType=payload.ReportType,
        section=payload.SectionName,
    )


# Get Financial Higlights Section Tables
@FinancialHighlights.post("/get/financialHeights/tables")
def getTables(payload: SectionChartRequestData) -> Result:
    return getISTable(
        year=payload.Year,
        months=payload.Months,
        reportType=payload.ReportType,
        section=payload.SectionName,
    )
