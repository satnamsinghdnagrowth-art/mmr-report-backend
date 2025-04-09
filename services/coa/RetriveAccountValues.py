from helper.readExcel import readExcelFile
from datetime import datetime
from core.models.base.ResultModel import Result


# Analyze the data
def retriveAccountValues(accountName : str):
    try:

        filePath = "tempFiles/Honest Game Corporation Jan 2025 (4).xlsx"

        excelData = readExcelFile(filePath)

        data = excelData.Data

        cleanedData = data[~data["Classification"].isnull()]

        matches = cleanedData[cleanedData["Account Name"] == accountName]

        matches = matches.drop(columns=["Classification", "Account Name"])

        return Result(
            Data=matches.to_dict(orient="records"), Status=1, Message="Success"
        )

    except Exception as ex:
        message = f"Error occur at readExcelFile: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
