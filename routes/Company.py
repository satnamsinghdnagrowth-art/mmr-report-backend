from fastapi import APIRouter
from core.models.base.ResultModel import Result
from core.models.base.SectionDataRequestBody import SectionChartRequestData
from services.reportSection.expensesAnalysis.sectionData.SectionData import (
    getSectionData,
)

CompanyRouter = APIRouter()


# # Get Financial Higlights Section All Data
@CompanyRouter.post("/get/company/", response_model=Result)
def createCompany(reportId: int, payload: SectionChartRequestData):
    return companyCreation(
        reportId=reportId,
        year=payload.Year,
        months=payload.Months,
        reportType=payload.ReportType,
        section=payload.SectionName,
    )
