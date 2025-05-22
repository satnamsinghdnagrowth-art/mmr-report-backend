from fastapi import APIRouter, Body, UploadFile, File
from core.models.base.ResultModel import Result
from services.accountValues.GetFinancialsValues import formatFinancialData
from services.fileUploadHandling.FileUpload import fileUpload


dataFormat = APIRouter()


# Format Excel Data
@dataFormat.get("/format/excel")
def formatReportData() -> Result:
    filePath = "tempFiles/Honest Game Corporation Jan 2025 (4).xlsx"
    return formatFinancialData(filePath, "HonestGameData")


@dataFormat.post("/upload")
def formatReportData(file: UploadFile = File(...)) -> Result:
    return fileUpload(file)
