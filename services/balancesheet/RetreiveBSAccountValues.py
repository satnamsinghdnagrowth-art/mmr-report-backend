from helper.readExcel import readExcelFile
from datetime import datetime
from core.models.base.ResultModel import Result


# Analyze the data
def retriveBSAccountValues(accountName: str):
    try:
        filePath = "tempFiles/Honest Game Corporation Jan 2025 (4).xlsx"

        excelData = readExcelFile(filePath)

        data = excelData.Data

        cleanedData = data[~data["Classification"].isnull()]

        matches = cleanedData[cleanedData["Classification"] == accountName]

        matches = matches.drop(columns=["Classification", "Account Name"])

        month_cols = [
            col
            for col in matches.columns
        ]

        # Create a dictionary with total revenue for each month
        monthly_totals = {
            month: matches[month].fillna(0).sum() for month in month_cols
        }

        return Result(Data=monthly_totals, Status=1, Message="Success")

    except Exception as ex:
        message = f"Error occur at readExcelFile: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
