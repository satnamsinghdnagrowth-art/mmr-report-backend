from fastapi import APIRouter, Body, UploadFile, File,Form
from core.models.base.ResultModel import Result
from services.accountValues.GetFinancialsValues import formatFinancialData
from services.fileUploadHandling.FileUpload import fileUpload
from typing import Optional

dataFormat = APIRouter()


# Format Excel Data
@dataFormat.get("/format/excel")
def formatReportData() -> Result:
    filePath = "tempFiles/Honest Game Corporation Jan 2025 (4).xlsx"
    return formatFinancialData(filePath, "HonestGameData")

# File upload endpoint
@dataFormat.post("/upload")
def formatReportData(
    file: Optional[UploadFile] = File(None),
    FileBase64Str: Optional[str] = Form(None)
) -> Result:
    if not file and not FileBase64Str:
        return Result(Status=400, Message="Either file or FileBase64Str must be provided.")
    
    return fileUpload(file,FileBase64Str)