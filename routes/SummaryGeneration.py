from fastapi import APIRouter
from core.models.base.SectionDataRequestBody import SectionRequestData
from services.reportSection.financialHighlights.tables.IncomeStatementTablesKPI import (
    getISTable,
)
from pydantic.json import pydantic_encoder
import json
from services.generateSummary.ExecutiveSummaryGenerator import generateExecutiveSummary

SummaryGeneratorRouter = APIRouter()


# Generate Executive Summary
@SummaryGeneratorRouter.post("/complete/report/{reportId}")
def generateReportSummary(reportId: int, payload: SectionRequestData):
    data = getISTable(
        payload.Year,
        payload.Months,
        payload.ReportType,
        payload.SectionName,
        reportId,
    ).Data

    compact_json = json.dumps(
        data, default=pydantic_encoder, separators=(",", ":"), ensure_ascii=False
    )

    responseData = generateExecutiveSummary(compact_json)

    return responseData
