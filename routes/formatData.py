from fastapi import APIRouter, Body, UploadFile, File,Form
from core.models.base.ResultModel import Result
from services.accountValues.GetFinancialsValues import formatFinancialData
from services.fileUploadHandling.FileUpload import fileUpload
from typing import Optional

dataFormat = APIRouter()

# File upload endpoint
@dataFormat.post("/upload",response_model=Result)
def formatReportData(
    file: Optional[UploadFile] = File(None),
    FileBase64Str: Optional[str] = Form(None)
):
    if not file and not FileBase64Str:
        return Result(Status=400, Message="Either file or FileBase64Str must be provided.")
    
    return fileUpload(file,FileBase64Str)