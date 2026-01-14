from core.models.base.ResultModel import Result
import json
import os
import traceback
from datetime import datetime
from helper.SaveCustomKpisList import getCustomKpisList
from config.FilesBaseDIR import CUSTOM_KPIS_DATA_UPLOAD_DIR

REPORT_JSON_PATH = "database/ReportTable.json"


def addCustomKPI(reportId: int, payload) -> Result:
    try:
        # Validate / fetch existing KPI list
        getCustomKpisList(reportId)

        customReportData = {
            "ReportId": reportId,
            "CustomKpi": payload.dict()
        }

        print(customReportData)

        report_json_path = (
            f"{CUSTOM_KPIS_DATA_UPLOAD_DIR}/{reportId}/customKpisData.json"
        )

        # Ensure directory exists
        os.makedirs(os.path.dirname(report_json_path), exist_ok=True)

        # Load existing data safely
        existing_data = []
        if os.path.exists(report_json_path):
            try:
                with open(report_json_path, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
                    if not isinstance(existing_data, list):
                        existing_data = []
            except json.JSONDecodeError:
                existing_data = []

        # Append new KPI data
        existing_data.append(customReportData)

        # Save updated data
        with open(report_json_path, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=4)

        return Result(
            Data=customReportData,
            Status=1,
            Message="KPI added successfully."
        )

    except Exception as ex:
        error_trace = traceback.format_exc()
        message = f"Error occurred in customKPICreation: {ex}"

        print(f"{datetime.now()} {message}")
        print(error_trace)

        return Result(
            Status=0,
            Message=message
        )
