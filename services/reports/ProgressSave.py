from datetime import datetime
from core.models.base.ResultModel import Result
from helper.LoadJsonData import SECTION_CARD_CONFIGS
from services.visuals.card.retrieveCard import retrieveCard
from datetime import datetime
import os
import json
from config.FilesBaseDIR import REPORT_META_DATA_JSON_PATH


def reportProgressSave(metaData):
    try:
        reportId = metaData["reportId"]
        file_path = f"{REPORT_META_DATA_JSON_PATH}/{reportId}.json"

        # Save back to file
        with open(file_path, "w") as f:
            json.dump(metaData, f, indent=4)

        return Result(Status=1, Message="Executive Summary Saved Successfully")

    except Exception as ex:
        message = f"Error occurred at reportProgressSave: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
