from fastapi import APIRouter
from core.models.base.ResultModel import Result
from core.models.base.SectionDataRequestBody import SectionChartRequestData
from services.reportSection.consolidateSection.ConsolidateDataReporting import (
    getConsolidateSectionData,
)

# Router Name
ConsolidateSectionsData = APIRouter()

@ConsolidateSectionsData.post(
    "/get/report/{reportId}/sectionData/", response_model=Result
)
def getSection(reportId: int, payload: SectionChartRequestData):
    return getConsolidateSectionData(
        reportId=reportId,
        year=payload.Year,
        months=payload.Months,
        reportType=payload.ReportType,
        section=payload.SectionName,
    )
