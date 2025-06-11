from fastapi import APIRouter
from core.models.base.ResultModel import Result
from core.models.base.SectionDataRequestBody import SectionChartRequestData
from services.reportSection.financialHighlights.sectionData.SectionData import (
    FinancialHighlightSectionDataService,
)

FinancialHighlights = APIRouter()


@FinancialHighlights.post("/get/report/{reportId}/sectionData/",response_model=Result)
def getSection(reportId: int, payload: SectionChartRequestData):
    return FinancialHighlightSectionDataService(
        reportId=reportId,
        year=payload.Year,
        months=payload.Months,
        reportType=payload.ReportType,
        section=payload.SectionName,
    ).get()


# Get Financial Higlights Section Cards
@FinancialHighlights.post("/get/report/{reportId}/cards",response_model=Result)
def getCards(reportId: int, payload: SectionChartRequestData):
    return FinancialHighlightSectionDataService(
        reportId=reportId,
        year=payload.Year,
        months=payload.Months,
        reportType=payload.ReportType,
        section=payload.SectionName,
    ).getCardsOnly()


# Get Financial Higlights Section Charts
@FinancialHighlights.post("/get/report/{reportId}/charts",response_model=Result)
def getCharts(reportId: int, payload: SectionChartRequestData):
    return FinancialHighlightSectionDataService(
        reportId=reportId,
        year=payload.Year,
        months=payload.Months,
        reportType=payload.ReportType,
        section=payload.SectionName,
    ).getChartsOnly()


# Get Financial Higlights Section Tables
@FinancialHighlights.post("/get/report/{reportId}/tables",response_model=Result)
def getTables(reportId: int, payload: SectionChartRequestData):
    return FinancialHighlightSectionDataService(
        reportId=reportId,
        year=payload.Year,
        months=payload.Months,
        reportType=payload.ReportType,
        section=payload.SectionName,
    ).getTablesOnly()
