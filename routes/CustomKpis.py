from fastapi import APIRouter
from core.models.base.ResultModel import Result
from core.models.base.SectionDataRequestBody import SectionRequestData
from services.customKPIs.CustomKPIsCreation import customKPICreation
from core.models.visualsModel.CustomKpiModel import CustomKpiRequestModel


CustomKPIsRouter = APIRouter()


# # Get Financial Higlights Section All Data
@CustomKPIsRouter.post("/report/{reportId}/", response_model=Result)
def createCustomKPI(reportId: int, payload: CustomKpiRequestModel):
    return customKPICreation(payload, reportId)
