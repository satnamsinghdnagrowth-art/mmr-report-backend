from fastapi import APIRouter
from core.models.base.ResultModel import Result
from core.models.base.SectionDataRequestBody import SectionChartRequestData
from services.reportSection.profitAbility.tables.GetProfitAbilityTable import getPATable
from services.reportSection.profitAbility.charts.ProfitAbilityChart import getPACharts
from services.reportSection.profitAbility.sectionData.SectionData import getSectionData

BreakEvenAnaysis = APIRouter()


# # Get Financial Higlights Section All Data
@BreakEvenAnaysis.get("/get/sectionData")
def getCards()->Result:
    return getSectionData(
        year=2024,
        months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        reportType="Yearly",
        section="Financial Heights",
    )