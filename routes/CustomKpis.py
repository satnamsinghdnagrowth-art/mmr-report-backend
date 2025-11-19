from fastapi import APIRouter, UploadFile, File
from core.models.base.ResultModel import Result
from services.customKPIs.CustomKPIsCreation import customKPICreation
from core.models.visualsModel.CustomKpiModel import CustomKpiRequestModel
from services.customKPIs.CustomKPIsItems import customKpiItems
from typing import Optional
from services.customKPIs.CreateCustomKPIsList import addCustomKPI
from services.customKPIs.RawDataProcessing import customKPIsDataProcessing


CustomKPIsRouter = APIRouter()


# File Upload Router for Customs KPIs
@CustomKPIsRouter.post("/upload-data/report/{reportId}/", response_model=Result)
def formatReportData(reportId, file: Optional[UploadFile] = File(None)):
    if not file:
        #  and not FileBase64Str:
        return Result(
            Status=400, Message="Either file or FileBase64Str must be provided."
        )
    return customKPIsDataProcessing(file, reportId)


# Get Items of Custom Data
@CustomKPIsRouter.get("/get/items/report/{reportId}", response_model=Result)
def getcustomKpiItems(reportId: int):
    return customKpiItems(reportId)


# Get Custom Section All Data
@CustomKPIsRouter.post("/create/report/{reportId}/", response_model=Result)
def createCustomKPI(reportId: int, payload: CustomKpiRequestModel):
    return addCustomKPI(reportId, payload)
