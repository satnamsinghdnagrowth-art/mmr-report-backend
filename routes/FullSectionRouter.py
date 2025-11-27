from fastapi import APIRouter
from core.models.base.ResultModel import Result
from core.models.base.SectionDataRequestBody import SectionRequestData
from services.reportSection.consolidateSection.ConsolidateDataReporting import (
    getConsolidateSectionData,
)

# Router Name
ConsolidateDataRouter = APIRouter()


@ConsolidateDataRouter.post(
    "/get/report/{reportId}/sectionData/", response_model=Result
)
def getSection(reportId: int, payload: SectionRequestData):
    return getConsolidateSectionData(
        reportId=reportId,
        year=payload.Year,
        months=payload.Months,
        reportType=payload.ReportType,
        section=payload.SectionName,
        companyId=payload.CompanyId,
    )
