from datetime import datetime
from services.accountValues.RetriveCOAValues import retriveCOAValues
from core.models.base.ResultModel import Result
from helper.readExcel import readExcelFile
import json
import os
import shutil
from fastapi.encoders import jsonable_encoder

REPORT_JSON_PATH = "database/ReportTable.json"
REPORT_JSONL_PATH = "database/ReportTable.jsonl"

# Analyze the data
def formatFinancialData(filePath, reportId: int, companyLogo):
    try:
        fileName = os.path.splitext(os.path.basename(filePath))[0]

        excelData = readExcelFile(filePath, reportId)

        formattedData = excelData.Data

        reportDetails = formattedData["Report Details"]

        financialData = formattedData["Financial Data"]

        if companyLogo is not None:
            logoFileName = f"logo_{reportId}"
            fileExtension = ".png"
            timeStamp = datetime.now().strftime("%Y%m%d%H%M%S")

            savedFileName = f"{logoFileName}_{timeStamp}{fileExtension}"
            logoFilePath = os.path.join("database", "companyLogos", savedFileName)

            with open(logoFilePath, "wb") as buffer:
                shutil.copyfileobj(companyLogo.file, buffer)

        else:
            logoFilePath = "database/companyLogos/sample-logo.png"

        data = {
            "ReportId": reportId,
            "Report Details": reportDetails,
            "Financial Data": {
                "PROFIT & LOSS": retriveCOAValues(
                    financialData, category="PROFIT & LOSS"
                ).Data,
                "BalanceSheet": retriveCOAValues(
                    financialData, category="BALANCE SHEET"
                ).Data,
                "EQUITY": retriveCOAValues(financialData, category="EQUITY").Data,
            },
        }

        with open(f"database/reportsDataFiles/{fileName}.json", "w") as f:
            # json.dump(data, f, indent=4)
            json.dump(jsonable_encoder(data), f, indent=4)

        # 📦 Metadata object
        reportMetadata = {
            "ReportId": reportId,
            "ReportName": fileName.replace("_", " "),
            "FileName": f"{fileName}.json",
            "CompanyLogoFilePath": logoFilePath,
            "Currency": "US Dollar",
            "CreatedOn": datetime.now().isoformat(),
        }

        if os.path.exists(REPORT_JSON_PATH):
            with open(REPORT_JSON_PATH, "r") as f:
                existing_data = json.load(f)  # existing_data should be a list
        else:
            existing_data = []

        # Append new report metadata
        existing_data.append(reportMetadata)

        with open(REPORT_JSONL_PATH, "a", encoding="utf-8") as f:
             f.write(json.dumps(reportMetadata) + "\n")

        with open(REPORT_JSON_PATH, "w") as f:
            json.dump(existing_data, f, indent=4)

        return Result(Data=data, Status=1, Message="Success")

    except Exception as ex:
        message = f"Error occur at formatFinancialData: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
