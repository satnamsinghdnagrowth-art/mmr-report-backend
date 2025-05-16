from fastapi import APIRouter, Body,UploadFile,File
from core.models.base.ResultModel import Result
from services.accountValues.GetFinancialsValues import formatFinancialData
from services.fileUploadHandling.FileUpload import fileUpload


dataFormat = APIRouter()


# Format Excel Data
@dataFormat.get("/excel")
def formatReportData() -> Result:
    return formatFinancialData()


@dataFormat.post("/upload")
def formatReportData(file: UploadFile = File(...)) -> Result:
    return fileUpload(file)

