from core.models.base.ResultModel import Result
import json
import os
from datetime import datetime
from helper.SaveCustomKpisList import getCustomKpisList
from config.FilesBaseDIR import CUSTOM_KPIS_DATA_UPLOAD_DIR

REPORT_JSON_PATH = "database/ReportTable.json"


def addCustomKPI(reportId: int, payload) -> Result:
    try:
        getCustomKpisList(reportId)

        customReportData = {"ReportId": reportId, "CustomKpi": payload.dict()}

        print(customReportData)

        REPORT_JSON_PATH = (
            f"{CUSTOM_KPIS_DATA_UPLOAD_DIR}/{reportId}/customKpisData.json"
        )

        os.makedirs(os.path.dirname(REPORT_JSON_PATH), exist_ok=True)

        # Load existing data safely
        existing_data = []
        if os.path.exists(REPORT_JSON_PATH):
            try:
                with open(REPORT_JSON_PATH, "r") as f:
                    existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []

        existing_data.append(customReportData)

        # Save updated data
        with open(REPORT_JSON_PATH, "w") as f:
            json.dump(existing_data, f, indent=4)

        return Result(
            Data=customReportData, Status=1, Message="KPI added successfully."
        )

    except Exception as ex:
        message = f"Error occurred in customKPICreation: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
