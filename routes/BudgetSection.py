from fastapi import APIRouter,UploadFile,File
from core.models.base.ResultModel import Result
from typing import Optional
from services.budget.rawDataProcessing import fileUploadProcessing
from helper.LoadJsonData import SECTION_CARD_CONFIGS


BudgetSectionRouter = APIRouter()


# Get Financial Higlights Section All Data
@BudgetSectionRouter.post("/get/report/{reportId}/sectionData/")
def formatBudgetData(reportId,file: Optional[UploadFile] = File(None)):
    if not file:
    #  and not FileBase64Str:
        return Result(
            Status=400, Message="Either file or FileBase64Str must be provided."
        )
    return fileUploadProcessing(file, reportId)