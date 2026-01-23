from datetime import datetime
import os
import json

from core.models.base.ResultModel import Result
from config.FilesBaseDIR import REPORT_META_DATA_JSON_PATH


def reportProgressSave(metaData: dict) -> Result:
    try:
        # print(f"{datetime.now().isoformat()} | reportProgressSave called with reportId: {metaData.get('reportId')}")
        # print(f"{datetime.now().isoformat()} | metaData content: {json.dumps(metaData, indent=2)}")
        # Validate required key
        reportId = metaData.get("reportId")
        if not reportId:
            return Result(Status=0, Message="reportId is missing in metaData")

        # Ensure directory exists
        os.makedirs(REPORT_META_DATA_JSON_PATH, exist_ok=True)

        file_path = os.path.join(REPORT_META_DATA_JSON_PATH, f"{reportId}.json")

        # Save JSON safely
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(
                metaData,
                f,
                indent=4,
                default=str  # handles datetime or other non-serializable objects
            )

        return Result(Status=1, Message="Executive Summary Saved Successfully")

    except Exception as ex:
        message = f"Error occurred at reportProgressSave: {ex}"
        print(f"{datetime.now().isoformat()} | {message}")
        return Result(Data=None, Status=0, Message=message)
