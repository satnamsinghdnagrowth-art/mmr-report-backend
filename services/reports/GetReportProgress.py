from datetime import datetime
from core.models.base.ResultModel import Result
from helper.LoadJsonData import SECTION_CARD_CONFIGS
from services.visuals.card.retrieveCard import retrieveCard
from datetime import datetime
import os
import json
from config.FilesBaseDIR import REPORT_META_DATA_JSON_PATH


# Get the sections cards
def getreportProgress(reportId: int, templateId: int):
    try:
        metaFilePath = f"{REPORT_META_DATA_JSON_PATH}/{reportId}.json"

        if os.path.exists(metaFilePath):
            with open(metaFilePath, "r") as f:
                existing_data = json.load(f)
                return Result(
                    Data=existing_data,
                    Status=1,
                    Message="Executive Summary Saved Successfully",
                )

        if templateId is not None:
            template_data_path = "config/CompanyBaseComponents/HeyBegal.json"
            with open(template_data_path, "r") as f:
                existing_data = json.load(f)
                return Result(
                    Data=existing_data,
                    Status=1,
                    Message="Executive Summary Saved Successfully",
                )

        else:
            return Result(
                Status=1,
                Message="Data not avaible, user has choosen to create report from scratch",
            )

    except Exception as ex:
        message = f"Error occurred at getFHSectionCards: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
