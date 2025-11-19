from fastapi import APIRouter
from pydantic import BaseModel
from core.models.base.ResultModel import Result
from services.reports.ProgressSave import reportProgressSave
from services.ExtractDataRange import retriveDataRange

Analyze = APIRouter()


class SummaryObject(BaseModel):
    ReportId: int
    Summary: dict


@Analyze.get("/{reportId}", response_model=Result)
def analyzeData(reportId: int):
    return retriveDataRange(reportId)


@Analyze.post("/saveSummary", response_model=Result)
def saveReportProgress(metaData: dict):
    return reportProgressSave(metaData)
