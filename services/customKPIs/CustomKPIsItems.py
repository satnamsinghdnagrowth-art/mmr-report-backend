from core.models.base.ResultModel import Result
import json
from datetime import datetime
from services.customKPIs.visualCreation.CustomChartCreation import format_chart_data
from services.customKPIs.visualCreation.CustomTableCreation import format_table_data
from services.customKPIs.visualCreation.CustomCardCreation import format_card_data
from config.FilesBaseDIR import CUSTOM_KPIS_DATA_UPLOAD_DIR
import os

REPORT_JSON_PATH = "database/ReportTable.json"


# Custom
def customKpiItems(reportId: int) -> Result:
    try:
        customFilePath = None

        report_list_path = REPORT_JSON_PATH  # your master JSON list

        if os.path.exists(report_list_path):
            with open(report_list_path, "r") as f:
                reports = json.load(f)

            for item in reports:
                if item["ReportId"] == int(reportId):
                    customFilePath = item["CustomKPIFilePath"]
                    break

        with open(customFilePath) as f:
            data = json.load(f)

        filteredData = data["Custom KPIs"].keys()

        # Return raw filtered data for other visual types
        return Result(
            Data=list(filteredData), Status=1, Message="Data filtered successfully."
        )

    except Exception as ex:
        message = f"Error occurred in customKPICreation: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
