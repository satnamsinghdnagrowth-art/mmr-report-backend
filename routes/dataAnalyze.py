from fastapi import APIRouter
from core.models.base.ResultModel import Result
from services.ExtractDataRange import retriveDataRange

Analyze = APIRouter()

# @Analyze.get("/")
# def analyzeData():
#     return retriveDataRange()



@Analyze.get("/{reportId}",response_model=Result)
def analyzeData(reportId:int):
    return retriveDataRange(reportId)
