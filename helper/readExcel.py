import pandas as pd
from datetime import datetime
from core.models.base.ResultModel import Result


# Read the excel File
def readExcelFile(filepath) -> Result:
    try:
        excelData = pd.read_excel(filepath, header=4)

        # reportName = excelData.iloc[0, 1]
        # financialYear = excelData.iloc[1, 1]

        # header = excelData.iloc[3]
        # data = excelData.iloc[4:].reset_index(drop=True)
        # data.columns = header  # Set proper headers

        # response = {
        #     "Company Name":reportName,
        #     "Financial Year":financialYear,
        #     "Financial Data":data
        # }

        return Result(Data=excelData, Status=0, Message="SUCCESS")

    except Exception as ex:
        message = f"Error occur at readExcelFile: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
