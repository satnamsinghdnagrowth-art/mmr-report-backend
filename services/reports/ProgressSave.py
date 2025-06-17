from datetime import datetime
from core.models.base.ResultModel import Result
from helper.LoadJsonData import SECTION_CARD_CONFIGS
from services.visuals.card.retrieveCard import retrieveCard
from datetime import datetime
import os
import json
from config.FilesBaseDIR import PROGRESS_JSON_PATH


# Get the sections cards
def reportProgressSave(payloadData):
    try:
        if os.path.exists(PROGRESS_JSON_PATH):
            with open(PROGRESS_JSON_PATH, "r") as f:
                existing_data = json.load(f)  # existing_data should be a list
        else:
            existing_data = []


        # Append new report metadata
        existing_data.append(payloadData.dict())
        
        with open(PROGRESS_JSON_PATH, "w") as f:
            json.dump(existing_data, f, indent=4)

        return Result( Status=1, Message="Executive Summary Saved Successfully"
        )

    except Exception as ex:
        message = f"Error occurred at getFHSectionCards: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
