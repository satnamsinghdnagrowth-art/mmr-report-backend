from datetime import datetime
from services.accountValues.RetriveCOAValues import retriveCOAValues
from core.models.base.ResultModel import Result
from helper.readExcel import readExcelFile
import json
import os
import random

REPORT_JSON_PATH = "database/ReportTable.json"


# Analyze the data
def formatFinancialData(filePath, fileName):
    try:
        # filePath = "tempFiles/Honest Game Corporation Jan 2025 (4).xlsx"

        excelData = readExcelFile(filePath)
        data = excelData.Data["Financial Data"]

        data = {
            "PROFIT & LOSS": retriveCOAValues(data, category="PROFIT & LOSS").Data,
            "BalanceSheet": retriveCOAValues(data, category="BALANCE SHEET").Data,
            "EQUITY": retriveCOAValues(data, category="EQUITY").Data,
        }

        with open(f"database/reportsDataFiles/{fileName}.json", "w") as f:
            json.dump(data, f, indent=4)

        reportId = str(random.randint(10000, 99999))

        # 📦 Metadata object
        report_metadata = {
            reportId: {
                "Report Name": fileName.replace("_", " "),
                "FileName": f"{fileName}.json",
                "Currency": "US Dollar",
            }
        }

        if os.path.exists(REPORT_JSON_PATH):
            with open(REPORT_JSON_PATH, "r") as f:
                existing_data = json.load(f)
        else:
            existing_data = {}

        existing_data.update(report_metadata)

        with open(REPORT_JSON_PATH, "w") as f:
            json.dump(existing_data, f, indent=4)

        return Result(Data=data, Status=1, Message="Success")

    except Exception as ex:
        message = f"Error occur at formatFinancialData: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
