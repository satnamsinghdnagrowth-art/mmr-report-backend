from datetime import datetime
from core.models.base.ResultModel import Result
from services.calculations.Ebit import EBIT
from services.calculations.Revenue import totalRevenue
from helper.LoadJsonData import financialDataTest
from helper.GetFileByReportId import getReportData
from typing import Optional
import os
import shutil
from datetime import datetime
import random
import json


from services.accountValues.GetFinancialsValues import formatFinancialData

UPLOAD_DIR = "database/uploadedFiles"


# Operating Profit
def fileUpload(file):
    try:
        timeStamp = datetime.now()

        fileFullName = os.path.splitext(file.filename)

        fileExtension = fileFullName[1]

        # Accepts Only Excel File
        if fileExtension not in [".xlsx", "xls"]:
            return Result(Status=0, Message="Please Upload an Excel File..........")

        fileNameOnly = fileFullName[0]

        savedFileName = f"{fileNameOnly}_{timeStamp}{fileExtension}"

        filePath = os.path.join(UPLOAD_DIR, savedFileName)

        # Save the file
        with open(filePath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        dataFormat = formatFinancialData(filePath, fileNameOnly)

        return Result(
            Data="fileUpload",
            Status=1,
            Message="File upladed Successfully",
        )

    except Exception as ex:
        message = f"Error occur at fileUpload: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
