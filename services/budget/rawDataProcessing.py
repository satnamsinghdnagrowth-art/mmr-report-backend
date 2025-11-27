from datetime import datetime
from core.models.base.ResultModel import Result
from helper.LoadJsonData import financialDataTest
from helper.GetFileByReportId import getReportData
import os
from datetime import datetime
from core.models.base.ResultModel import Result
import random
from services.budget.dataFormatting import formatFinancialData
from helper.Base64FileHandler import handleBase64File
from helper.FileUploadHandler import handleUploadFile
from config.FilesBaseDIR import BUDGET_DATA_UPLOAD_DIR


def fileUploadProcessing(file, reportId, fileBase64Str=None):
    try:
        fileNameOnly = f"BudgetFile_{reportId}"

        fileExtension = ".xlsx"  # or parse from `header` if possible

        # === CASE 1: Uploaded File ===
        if file is not None:
            savedFilePath = handleUploadFile(
                file, fileNameOnly, fileExtension, BUDGET_DATA_UPLOAD_DIR
            ).Data

        # === CASE 2: Base64 File ===
        if fileBase64Str is not None:
            savedFilePath = handleBase64File(
                fileBase64Str, fileNameOnly, fileExtension, BUDGET_DATA_UPLOAD_DIR
            ).Data

        result = formatFinancialData(savedFilePath, reportId)

        if result.Status == 1:

            return Result(
                Status=1,
                Message="Budget File uploaded Successfully",
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
