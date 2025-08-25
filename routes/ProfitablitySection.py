from fastapi import APIRouter
from core.models.base.ResultModel import Result
from core.models.base.SectionDataRequestBody import SectionChartRequestData
from services.reportSection.profitAbility.tables.GetProfitAbilityTable import getPATable
from services.visuals.charts.GetSectionCharts import getSectionCharts
from services.reportSection.profitAbility.sectionData.SectionData import getSectionData

ProfitAbility = APIRouter()


# # Get Financial Higlights Section All Data
@ProfitAbility.post("/get/report/{reportId}/sectionData", response_model=Result)
def getSection(reportId: int, payload: SectionChartRequestData):
    return getSectionData(
        reportId=reportId,
        year=payload.Year,
        months=payload.Months,
        reportType=payload.ReportType,
        section=payload.SectionName,
    )


# def getCards()->Result:
#     return getSectionData(
#         year=2024,
#         months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
#         reportType="Year",
#         section="Financial Heights",
#     )


# # Get Financial Higlights Section Charts
@ProfitAbility.post("/get/charts", response_model=Result)
def getCards(payload: SectionChartRequestData):
    return getSectionCharts(
        year=payload.Year,
        months=payload.Months,
        reportType=payload.ReportType,
        section=payload.SectionName,
    )


# Get Financial Higlights Section Tables
@ProfitAbility.post("/get/tables", response_model=Result)
def getTables(payload: SectionChartRequestData):
    return getPATable(
        year=payload.Year,
        months=payload.Months,
        reportType=payload.ReportType,
        section=payload.SectionName,
    )
