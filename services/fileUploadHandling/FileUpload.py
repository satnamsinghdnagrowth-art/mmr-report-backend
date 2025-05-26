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
import base64
from services.accountValues.GetFinancialsValues import formatFinancialData
from helper.Base64FileHandler import handleBase64File
from helper.FileUploadHandler import handleUploadFile


UPLOAD_DIR = "database/uploadedFiles"


def fileUpload(file,fileBase64Str):
    try:

        reportId = random.randint(10000, 99999)

        fileNameOnly = f"BaseFile_{reportId}"

        fileExtension = ".xlsx"  # or parse from `header` if possible

        # === CASE 1: Uploaded File ===
        if file is not None:
            savedFilePath = handleUploadFile(file,fileNameOnly,fileExtension).Data

        # === CASE 2: Base64 File ===
        if fileBase64Str is not None:
            savedFilePath = handleBase64File(fileBase64Str,fileNameOnly,fileExtension).Data

        result = formatFinancialData(savedFilePath, reportId)

        if result.Status == 1 :

            response = {
                "ReportId": result.Data["ReportId"]
            }

            return Result(
                Data=response,
                Status=1,
                Message="File uploaded Successfully",
            )
        
        if os.path.exists(savedFilePath):
            os.remove(savedFilePath)
        
        return Result(
                Status=0,
                Message="Please Uplaoded the correct file format.",
            ) 

    except Exception as ex:
        message = f"Error occur at fileUpload: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
