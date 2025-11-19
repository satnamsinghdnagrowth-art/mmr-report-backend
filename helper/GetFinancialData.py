from core.models.base.SourceModel import SourceDataTypes
from helper.GetFileByReportId import getReportData,getBudgetData

def getFinancialData(reportId, dataType):
    if dataType == SourceDataTypes.Actuals:
        return getReportData(reportId).get("Financial Data", {})

    if dataType == SourceDataTypes.Budget:
        return getBudgetData(reportId).get("Financial Data", {})

    # fallback or test data
    return None
