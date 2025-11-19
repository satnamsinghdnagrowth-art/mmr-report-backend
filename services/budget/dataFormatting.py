from datetime import datetime
from services.accountValues.RetriveCOAValues import retriveCOAValues
from core.models.base.ResultModel import Result
from helper.readExcel import readExcelFile
import json
import os
import shutil
from fastapi.encoders import jsonable_encoder

REPORT_JSON_PATH = "database/ReportTable.json"


# Analyze the data
def formatFinancialData(filePath, reportId: int):
    try:
        fileName = os.path.splitext(os.path.basename(filePath))[0]

        excelData = readExcelFile(filePath, reportId)

        formattedData = excelData.Data

        reportDetails = formattedData["Report Details"]

        financialData = formattedData["Financial Data"]

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

        output_dir = f"database/budgetDataFiles/{reportId}"
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, f"BudgetFile_{reportId}.json")
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

        report_list_path = REPORT_JSON_PATH

        if os.path.exists(report_list_path):
            with open(report_list_path, "r") as f:
                reports = json.load(f)

            updated = False
            for item in reports:
                if item["ReportId"] == int(reportId):
                    item["BudgetFilePath"] = output_path.replace("\\", "/")
                    updated = True
                    break

            if not updated:
                raise ValueError(f"ReportId {reportId} not found in reports.json")

            with open(report_list_path, "w") as f:
                json.dump(reports, f, indent=4)
        else:
            raise FileNotFoundError("reports.json file not found in 'database/' folder")

        return Result(
            Status=1, Message="Data formatted successfully and report list updated."
        )

    except Exception as ex:
        message = f"Error occur at formatFinancialData: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
