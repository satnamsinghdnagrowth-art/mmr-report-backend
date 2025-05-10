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


@FinancialHighlights.post("/get/report/{reportId}/sectionData/")
def getSection(reportId: int, payload: SectionChartRequestData) -> Result:
    return getSectionData(
        reportId=reportId,
        year=payload.Year,
        months=payload.Months,
        reportType=payload.ReportType,
        section=payload.SectionName,
    )


# Get Financial Higlights Section All Data
# @FinancialHighlights.post("/get/report/{reportId}/sectionData/")
# def getSection(payload: SectionChartRequestData) -> Result:
#     return getSectionData(
#         year=payload.Year,
#         months=payload.Months,
#         reportType=payload.ReportType,
#         section=payload.SectionName,
#     )


# Get Financial Higlights Section Cards
@FinancialHighlights.post("/get/report/{reportId}/cards")
def getCards(reportId: int, payload: SectionChartRequestData) -> Result:
    return getSectionCards(
        reportId=reportId,
        year=payload.Year,
        months=payload.Months,
        reportType=payload.ReportType,
        section=payload.SectionName,
    )


# Get Financial Higlights Section Charts
@FinancialHighlights.post("/get/report/{reportId}/charts")
def getCards(reportId: int, payload: SectionChartRequestData) -> Result:
    return getSectionCharts(
        reportId=reportId,
        year=payload.Year,
        months=payload.Months,
        reportType=payload.ReportType,
        section=payload.SectionName,
    )


# Get Financial Higlights Section Tables
@FinancialHighlights.post("/get/report/{reportId}/tables")
def getTables(reportId: int, payload: SectionChartRequestData) -> Result:
    return getISTable(
        reportId=reportId,
        year=payload.Year,
        months=payload.Months,
        reportType=payload.ReportType,
        section=payload.SectionName,
    )
