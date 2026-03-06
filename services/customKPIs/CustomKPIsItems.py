from core.models.base.ResultModel import Result
from config.FilesBaseDIR import CUSTOM_KPIS_DATA_UPLOAD_DIR
from datetime import datetime
import json
import os


def _custom_kpi_data_path(reportId) -> str:
    return os.path.join(CUSTOM_KPIS_DATA_UPLOAD_DIR, str(reportId), f"CustomFile_{reportId}.json")


def customKpiItems(reportId: int) -> Result:
    try:
        file_path = _custom_kpi_data_path(reportId)

        if not os.path.exists(file_path):
            return Result(
                Data=[],
                Status=0,
                Message="No custom KPI data file found. Please upload a custom KPI Excel file first.",
            )

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        kpi_names = list(data.get("Custom KPIs", {}).keys())

        return Result(Data=kpi_names, Status=1, Message="Custom KPI items retrieved successfully.")

    except Exception as ex:
        message = f"Error occurred in customKpiItems: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
