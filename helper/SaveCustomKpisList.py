from config.FilesBaseDIR import CUSTOM_KPIS_DATA_UPLOAD_DIR
from core.models.visualsModel.CustomKpiModel import CustomKpiRequestModel
import json
import os

CustomKpisList = {}


def loadCustomKpisForReport(reportId: int):
    """
    Load custom KPIs for a specific report with caching.
    Loads from file on first access, then caches in memory.
    """
    global CustomKpisList

    # Return cached data if available
    if reportId in CustomKpisList:
        return CustomKpisList[reportId]

    try:
        REPORT_JSON_PATH = (
            f"{CUSTOM_KPIS_DATA_UPLOAD_DIR}/{reportId}/customKpisData.json"
        )

        # Check if file exists
        if not os.path.exists(REPORT_JSON_PATH):
            CustomKpisList[reportId] = []
            return []

        # Load from file
        with open(REPORT_JSON_PATH, "r") as f:
            data = json.load(f)

        # Filter and create model objects
        filteredData = [
            CustomKpiRequestModel(**kpi["CustomKpi"])
            for kpi in data
            if kpi.get("ReportId") == reportId
        ]

        # Cache in memory
        CustomKpisList[reportId] = filteredData

        return filteredData

    except Exception as ex:
        print(f"Error loading custom KPIs for report {reportId}: {ex}")
        CustomKpisList[reportId] = []
        return []


def getCustomKpisList(reportId):
    """
    Always reads from disk (no cache) so newly uploaded Excel data is
    immediately visible without a backend restart.
    """
    try:
        REPORT_JSON_PATH = (
            f"{CUSTOM_KPIS_DATA_UPLOAD_DIR}/{reportId}/customKpisData.json"
        )

        if not os.path.exists(REPORT_JSON_PATH):
            return None

        with open(REPORT_JSON_PATH, "r") as f:
            data = json.load(f)

        filteredData = [
            CustomKpiRequestModel(**kpi["CustomKpi"])
            for kpi in data
            if kpi["ReportId"] == reportId
        ]

        global CustomKpisList
        CustomKpisList[reportId] = filteredData

        return CustomKpisList

    except Exception as ex:
        print(f"Error occurred in getCustomKpisList: {ex}")
        return None
