from fastapi import APIRouter, Body
from core.models.base.ResultModel import Result
from services.accountValues.GetFinancialsValues import formatFinancialData


dataFormat = APIRouter()


# Format Excel Data
@dataFormat.get("/excel")
def formatReportData() -> Result:
    return formatFinancialData()
