from fastapi import APIRouter, Body, UploadFile, File,Form
from core.models.base.ResultModel import Result
from services.accountValues.GetFinancialsValues import formatFinancialData
from services.fileUploadHandling.FileUpload import fileUpload
from services.reports.UpdateReportData import updateReportFields
from typing import Optional

dataFormat = APIRouter()



# File upload endpoint
@dataFormat.post("/upload",response_model=Result)
def formatReportData(
    file: Optional[UploadFile] = File(None),
    FileBase64Str: Optional[str] = Form(None),
    CompanyLogo : Optional[UploadFile] = File(None)
):
    if not file and not FileBase64Str:
        return Result(Status=400, Message="Either file or FileBase64Str must be provided.")
    
    return fileUpload(file,FileBase64Str,CompanyLogo)

@dataFormat.patch("/update/report/{reportId}/")
def uploadLogo(reportId:int,CompanyLogo : Optional[UploadFile] = File(None)):
    return updateReportFields(reportId,CompanyLogo)
    

@dataFormat.get("/{reportId}",response_model=Result)
def analyzeData(reportId:int):
    return (reportId)
