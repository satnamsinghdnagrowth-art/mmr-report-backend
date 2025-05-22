import pandas as pd
from core.models.base.ResultModel import Result
import numpy as np


# def readExcelFile(filepath) -> Result:
#     try:
#         # Step 1: Read the entire file without headers to extract metadata
#         excelData = pd.read_excel(filepath, header=None)

#         # Step 2: Extract the report name and financial year from the first two rows
#         reportName = excelData.iloc[0, 1]
#         financialYear = excelData.iloc[1, 1]

#         # Step 3: Set the header row from row 4 (index 4) and reset the dataframe
#         headers = excelData.iloc[4]
        

#         data = excelData.iloc[5:].reset_index(drop=True)

#         # Step 4: Assign the headers to the dataframe
#         data.columns = headers


#         data = data.applymap(
#             lambda x: x.item() if isinstance(x, (np.int64, np.float64)) else x
#         )

#         # Step 5: Build the response with extracted metadata and data
#         response = {
#             "Report Details":
#                 { 
#                 "Company Name": reportName,
#                 "Financial Year": financialYear,
#                 "Data Range" : headers
#                 },
#             "Financial Data": data,
#         }

#         return Result(Data=response, Status=1, Message="SUCCESS")

#     except Exception as ex:
#         message = f"Error occurred at readExcelFile: {ex}"
#         return Result(Status=0, Message=message)


import pandas as pd
import numpy as np
from datetime import datetime
from core.models.Accounts.ReportDescriptionModel import ReportDescriptionsModel, DateObject
from core.models.base.ResultModel import Result


def readExcelFile(
    filePath: str
) -> Result:
    try:
        # Step 1: Read raw Excel without headers to extract metadata
        excelData = pd.read_excel(filePath, header=None)

        # Step 2: Extract metadata
        reportName = excelData.iloc[0, 1]
        financialYear = excelData.iloc[1, 1]

        # Step 3: Extract headers and data
        headers = excelData.iloc[4]
        data = excelData.iloc[5:].reset_index(drop=True)
        data.columns = headers

        # Optional conversion for consistency
        data = data.applymap(
            lambda x: x.item() if isinstance(x, (np.int64, np.float64)) else x
        )

        # Only return parsed data range as DateObjects
        monthlyHeaderRow = data[data["Account Name"] == "Account Name"]


        # if monthlyHeaderRow.empty:
        #     return Result(Status=0, Message="No monthly header row found")

        dataRangeFrame = monthlyHeaderRow.drop(
            columns=["Classification", "Account Name"], errors="ignore"
        )
        dataRange = list(dataRangeFrame.columns)

        converted_data_range = [
            DateObject(
                Month=datetime.strptime(label, "%b %Y").strftime("%B")[0:3],
                    # if monthAsString else datetime.strptime(label, "%b %Y").strftime("%b")),
                Year=datetime.strptime(label, "%b %Y").year,
            )
            for label in dataRange
        ]

        response = {
            "Report Details": {
                "Company Name": reportName,
                "Financial Year": financialYear,
                "Data Range": converted_data_range,
            },
            "Financial Data": data,
        }
        return Result(Data=response, Status=1, Message="SUCCESS")
            # return Result(Data=reportDescription, Status=1, Message="SUCCESS")

    except Exception as ex:
        message = f"Error occurred in extractExcelReportDetails: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
