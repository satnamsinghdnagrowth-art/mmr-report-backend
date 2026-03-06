from fastapi import APIRouter, Body, UploadFile, File, Form
from core.models.base.ResultModel import Result
from services.fileUploadHandling.FileUpload import fileUpload
from services.reports.UpdateReportData import updateReportFields
from typing import Optional
from weasyprint import HTML
from services.budget.rawDataProcessing import fileUploadProcessing
from services.customKPIs.RawDataProcessing import customKPIsDataProcessing


UploadRouter = APIRouter()

# <-------------------- Upload the Actuals Data---------------------->
@UploadRouter.post("/actuals", response_model=Result)
def formatReportData(
    file: Optional[UploadFile] = File(None),
    FileBase64Str: Optional[str] = Form(None),
    CompanyLogo: Optional[UploadFile] = File(None),
):
    if not file and not FileBase64Str:
        return Result(
            Status=400, Message="Either file or FileBase64Str must be provided."
        )
    return fileUpload(file, FileBase64Str, CompanyLogo)


# <-------------------- Upload the Budget Data---------------------->
@UploadRouter.post("/file/budget")
def formatBudgetData(reportId:int, file: Optional[UploadFile] = File(None)):
    if not file:
        #  and not FileBase64Str:
        return Result(
            Status=400, Message="Either file or FileBase64Str must be provided."
        )
    return fileUploadProcessing(file, reportId)


#<-------------------- Upload the Custom KPIs Data---------------------->
@UploadRouter.post("/custom", response_model=Result)
def formatReportData(reportId: int, file: Optional[UploadFile] = File(None)):
    if not file:
        #  and not FileBase64Str:
        return Result(
            Status=400, Message="Either file or FileBase64Str must be provided."
        )
    return customKPIsDataProcessing(file, reportId)


#<-------------------- Upload the  Report Logo---------------------->
@UploadRouter.patch("/logo")
def uploadLogo(reportId: int, CompanyLogo: Optional[UploadFile] = File(None)):
    return updateReportFields(reportId, CompanyLogo)
