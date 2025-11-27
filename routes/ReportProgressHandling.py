from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from core.models.base.ResultModel import Result
from services.reports.ProgressSave import reportProgressSave
from services.reports.GetReportProgress import getreportProgress


ReportProgressRouter = APIRouter()


# Save Report Progress
@ReportProgressRouter.post("/save/report", response_model=Result)
def saveReportProgress(metaData: dict):
    return reportProgressSave(metaData)


# Get the Progress Data
@ReportProgressRouter.get("/get/report/{reportId}", response_model=Result)
def saveReportProgress(reportId: int, templateId: Optional[int]=None):
    return getreportProgress(reportId, templateId)
