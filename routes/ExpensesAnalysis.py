from fastapi import APIRouter
from core.models.base.ResultModel import Result
from services.reportSection.expensesAnalysis.sectionData.SectionData import getSectionData

ExpensesAnalysis = APIRouter()


# # Get Financial Higlights Section All Data
@ExpensesAnalysis.get("/get/sectionData")
def getSections()->Result:
    return getSectionData(
        year=2024,
        months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        reportType="Yearly",
        section="Financial Heights",
    )


# # Get Financial Higlights Section Cards
# @ProfitAbility.post("/get/profitability/cards")
# def getCards(payload: SectionChartRequestData)-> Result:
#     return getSectionCards(
#         year=payload.Year,
#         months=payload.Months,
#         reportType=payload.ReportType,
#         section=payload.SectionName,
#     )


# # Get Financial Higlights Section Charts
# @ExpensesAnalysis.post("/get/charts")
# def getCards(payload: SectionChartRequestData) -> Result:
#     return getPACharts(
#         year=payload.Year,
#         months=payload.Months,
#         reportType=payload.ReportType,
#         section=payload.SectionName,
#     )


# # Get Financial Higlights Section Tables
# @ExpensesAnalysis.post("/get/tables")
# def getTables(payload: SectionChartRequestData) -> Result:
#     return getPATable(
#         year=payload.Year,
#         months=payload.Months,
#         reportType=payload.ReportType,
#         section=payload.SectionName,
#     )
