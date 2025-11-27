from fastapi import APIRouter
from core.models.base.ResultModel import Result
from core.models.base.SectionDataRequestBody import SectionRequestData
from services.reportSection.cashFlowAnalysis.sectionData.SectionData import (
    getSectionData,
)

CashFlowRouter = APIRouter()


# # Get Financial Higlights Section All Data
@CashFlowRouter.post("/get/report/{reportId}/sectionData", response_model=Result)
def getSection(reportId: int, payload: SectionRequestData):
    return getSectionData(
        reportId=reportId,
        year=payload.Year,
        months=payload.Months,
        reportType=payload.ReportType,
        section=payload.SectionName,
    )
