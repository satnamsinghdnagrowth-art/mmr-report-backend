from helper.readExcel import readExcelFile
from datetime import datetime
from collections import defaultdict
from config.variable import variableMapping
from core.models.base.ResultModel import Result


# Analyze the data
def retriveBSAccountNames():
    try:

        # accountType = "BalanceSheet"

        filePath = "tempFiles/Honest Game Corporation Jan 2025 (4).xlsx"

        excelData = readExcelFile(filePath)

        data = excelData.Data

        result = defaultdict(list)

        BSData = variableMapping["BALANCE SHEET"]

        for main, category in BSData.items():

            for code in category:
                    
                result[main].append({"name": list(code.values())[0]})

        return Result(Data=result, Status=1, Message="Success")

    except Exception as ex:
        message = f"Error occur at readExcelFile: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
