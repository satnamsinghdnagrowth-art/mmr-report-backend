from fastapi import APIRouter
from services.ExtractDataRange import retriveDataRange

Analyze = APIRouter()


@Analyze.get("/")
def analyzeData():
    return retriveDataRange()
