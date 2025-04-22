from fastapi import APIRouter
from services.ExtractDataRange import retriveDataRange
from utils.ReadSageExcel import testformat

Analyze = APIRouter()


@Analyze.get("/")
def analyzeData():
    return retriveDataRange()

@Analyze.get("/readData")
def analyzeData():
    return testformat()
