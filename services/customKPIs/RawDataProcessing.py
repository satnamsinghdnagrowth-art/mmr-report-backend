from helper.FileUploadHandler import handleUploadFile
from core.models.base.ResultModel import Result
from services.customKPIs.FormatData import dataFormatting
from datetime import datetime
import os
from config.FilesBaseDIR import CUSTOM_KPIS_DATA_UPLOAD_DIR


def customKPIsDataProcessing(file, reportId: int) -> Result:
    try:
        fileNameOnly = f"CustomKPIs_{reportId}"

        fileExtension = ".xlsx"  # or parse from `header` if possible

        if file is not None:
            savedFilePath = handleUploadFile(
                file, fileNameOnly, fileExtension, CUSTOM_KPIS_DATA_UPLOAD_DIR
            ).Data

        result = dataFormatting(savedFilePath)

        if result.Status == 1:
            response = {"Custom KPIs": result.Data["Custom KPIs"]}

            return Result(Data=response, Status=1, Message="File uploaded Successfully")

        if os.path.exists(savedFilePath):
            os.remove(savedFilePath)

        return Result(
            Status=0,
            Message="Please Uplaoded the correct file format.",
        )

    except Exception as ex:
        message = f"Error occurred in retriveDataRange: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
