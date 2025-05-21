import pandas as pd
from core.models.base.ResultModel import Result
import numpy as np


def readExcelFile(filepath) -> Result:
    try:
        # Step 1: Read the entire file without headers to extract metadata
        excelData = pd.read_excel(filepath, header=None)

        # Step 2: Extract the report name and financial year from the first two rows
        reportName = excelData.iloc[0, 1]
        financialYear = excelData.iloc[1, 1]

        # Step 3: Set the header row from row 4 (index 4) and reset the dataframe
        headers = excelData.iloc[4]

        data = excelData.iloc[5:].reset_index(drop=True)

        # Step 4: Assign the headers to the dataframe
        data.columns = headers


        data = data.applymap(
            lambda x: x.item() if isinstance(x, (np.int64, np.float64)) else x
        )

        # Step 5: Build the response with extracted metadata and data
        response = {
            "Company Name": reportName,
            "Financial Year": financialYear,
            "Financial Data": data,
        }

        return Result(Data=response, Status=1, Message="SUCCESS")

    except Exception as ex:
        message = f"Error occurred at readExcelFile: {ex}"
        return Result(Status=0, Message=message)
