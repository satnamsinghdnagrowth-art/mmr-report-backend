from fastapi import APIRouter
from core.models.base.ResultModel import Result
from core.models.base.SectionDataRequestBody import SectionChartRequestData
from services.reportSection.cashFlowAnalysis.sectionData.SectionData import (
    getSectionData,
)

CashFlow = APIRouter()


# # Get Financial Higlights Section All Data
@CashFlow.post("/get/report/{reportId}/sectionData",response_model=Result)
def getSection(reportId: int, payload: SectionChartRequestData):
    return getSectionData(
        reportId=reportId,
        year=payload.Year,
        months=payload.Months,
        reportType=payload.ReportType,
        section=payload.SectionName,
    )
