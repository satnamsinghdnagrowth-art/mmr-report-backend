from core.models.base.SourceModel import SourceDataTypes
from helper.GetFileByReportId import getReportData, getBudgetData
import os

def getFinancialData(reportId, dataType):
    if dataType == SourceDataTypes.Actuals:
        return getReportData(reportId).get("Financial Data", {})

    if dataType == SourceDataTypes.Budget:
        return getBudgetData(reportId).get("Financial Data", {})

    # fallback or test data
    return None


def checkFileExistance(filepath):
    if os.path.exists(filepath):
        return True
    else:
        return False