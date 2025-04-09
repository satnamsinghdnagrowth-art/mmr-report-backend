from fastapi import APIRouter
from services.DataAnalysis import analyze

Analyze = APIRouter()


@Analyze.get("/")
def analyzeData():
    return analyze()

