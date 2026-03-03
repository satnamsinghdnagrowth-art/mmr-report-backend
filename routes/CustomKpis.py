from fastapi import APIRouter, UploadFile, File
from core.models.base.ResultModel import Result
from core.models.visualsModel.CustomKpiModel import CustomKpiRequestModel
from services.customKPIs.CustomKPIsItems import customKpiItems
from typing import Optional
from services.customKPIs.CreateCustomKPIsList import addCustomKPI
from services.customKPIs.RawDataProcessing import customKPIsDataProcessing
from services.customKPIs.DeleteCustomKPI import deleteCustomKPI


CustomKPIsRouter = APIRouter()


# Get Items of Custom Data
@CustomKPIsRouter.get("/get/items/report/{reportId}", response_model=Result)
def getcustomKpiItems(reportId: int):
    return customKpiItems(reportId)


# Create / save a custom KPI visual definition
@CustomKPIsRouter.post("/create/report/{reportId}/", response_model=Result)
def createCustomKPI(reportId: int, payload: CustomKpiRequestModel):
    return addCustomKPI(reportId, payload)


# Delete a custom KPI visual definition by its visual ID
@CustomKPIsRouter.delete("/delete/report/{reportId}/kpi/{visual_id}", response_model=Result)
def removeCustomKPI(reportId: int, visual_id: str):
    return deleteCustomKPI(reportId, visual_id)
