from datetime import datetime
from services.accountValues.RetriveCOAValues import retriveCOAValues
from core.models.base.ResultModel import Result
from helper.readExcel import readExcelFile
import time
import json


# Analyze the data
def formatFinancialData():
    try:
        filePath = "tempFiles/Honest Game Corporation Jan 2025 (4).xlsx"
        excelData = readExcelFile(filePath)
        data = excelData.Data

        data = {
            "PROFIT & LOSS": retriveCOAValues(data, category="PROFIT & LOSS").Data,
            "BalanceSheet": retriveCOAValues(data, category="BALANCE SHEET").Data,
        }

        # with open("config/FileOutputTest.json", "w") as f:
        #     json.dump(data, f, indent=4)

        return Result(Data=data, Status=1, Message="Success")

    except Exception as ex:
        message = f"Error occur at retreiveNames: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
