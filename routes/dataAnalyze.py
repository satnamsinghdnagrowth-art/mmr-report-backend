from fastapi import APIRouter
from pydantic import BaseModel
from core.models.base.ResultModel import Result
from services.reports.ProgressSave import reportProgressSave
from services.ExtractDataRange import retriveDataRange

Analyze = APIRouter()


class SummaryObject(BaseModel):
    ReportId: int
    Summary: str


@Analyze.post("/saveSummary", response_model=Result)
def saveReportProgress(paylodData: SummaryObject):
    return reportProgressSave(paylodData)
