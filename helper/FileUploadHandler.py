from datetime import datetime
from core.models.base.ResultModel import Result
import os
import shutil
import base64
from services.accountValues.GetFinancialsValues import formatFinancialData


def handleUploadFile(
    file: str, fileNameOnly: str, fileExtension: SystemError, UPLOAD_DIR
):
    try:
        timeStamp = datetime.now().strftime(
            "%Y%m%d%H%M%S"
        )  # Format timestamp for filename safety

        if fileExtension.lower() not in [".xlsx", ".xls"]:
            return Result(Status=0, Message="Please upload an Excel file.")

        savedFileName = f"{fileNameOnly}_{timeStamp}{fileExtension}"
        filePath = os.path.join(UPLOAD_DIR, savedFileName)

        with open(filePath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return Result(
            Data=filePath,
            Status=1,
            Message="Total contribution calculated successfully",
        )

    except Exception as ex:
        message = f"Error occur at getValueSum: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
