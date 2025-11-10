import pandas as pd
from core.models.base.ResultModel import Result
import numpy as np
from datetime import datetime
from core.models.Accounts.ReportDescriptionModel import  DateObject
from core.models.base.ResultModel import Result
from core.models.base.SourceModel import SourceMetaDataModel
import os,json
from config.FilesBaseDIR import SOURCE_JSON_PATH

def readExcelFile(filePath: str,reportId:int) -> Result:
    try:
        pd.set_option("future.no_silent_downcasting", True)

        # Step 1: Read Excel with sheet names
        excelData = pd.read_excel(filePath, header=None, sheet_name=None)
        sheetName = list(excelData.keys())[0]
        sheetData = excelData[sheetName]

        # Step 2: Extract metadata
        reportName = sheetData.iloc[0, 1]
        financialMonth = sheetData.iloc[1, 1]
        financialMonthNumber = datetime.strptime(financialMonth, "%B").month

        # Step 3: Extract headers and data
        headers = sheetData.iloc[4]
        data = sheetData.iloc[5:].reset_index(drop=True)
        data.columns = headers

        # Optional conversion for numeric consistency
        data = data.applymap(
            lambda x: x.item() if isinstance(x, (np.int64, np.float64)) else x
        )

        # Extract date range
        monthlyHeaderRow = data[data["Account Name"] == "Account Name"]
        dataRangeFrame = monthlyHeaderRow.drop(
            columns=["Classification", "Account Name"], errors="ignore"
        )
        dataRange = [m for m in dataRangeFrame.columns if pd.notna(m)]

        converted_data_range = [
            DateObject(
                Month=(
                    label.month
                    if isinstance(label, datetime)
                    else datetime.strptime(label, "%b %Y").month
                ),
                Year=(
                    label.year
                    if isinstance(label, datetime)
                    else datetime.strptime(label, "%b %Y").year
                ),
            )
            for label in dataRange
        ]

        fileName = os.path.basename(filePath)

        # Filter valid rows (both Classification and Account Name not empty)
        df_valid = data.dropna(subset=["Classification", "Account Name"], how="any")

        # Total count of valid rows
        total_items = len(df_valid)

        # Group by Classification and make list of Account Names
        grouped = {
            cls: group["Account Name"].dropna().tolist()
            for cls, group in df_valid.groupby("Classification")
        }

        # Convert dict to list of dicts for Pydantic validation
        items_list = [
            { key: value}
            for key, value in grouped.items()
        ]

        # Create source metadata model
        sourceData = SourceMetaDataModel(
            SourceId=123456,
            ReportId=reportId,
            SourceName=fileName,
            SourceType="Excel",
            FilePath=filePath,
            SheetName=sheetName,
            TotalItems=total_items,
            ItemsList=items_list
        )

        # Final response
        response = {
            "Report Details": {
                "Company Name": reportName,
                "Financial Year": financialMonthNumber,
                "Data Range": converted_data_range,
            },
            "Financial Data": data
        }

        if os.path.exists(SOURCE_JSON_PATH):
            with open(SOURCE_JSON_PATH, "r") as f:
                existing_data = json.load(f)  # existing_data should be a list
        else:
            existing_data = []

        # Append new report metadata
        existing_data.append(sourceData.dict())

        with open(SOURCE_JSON_PATH, "w") as f:
            json.dump(existing_data, f, indent=4)

        return Result(Data=response, Status=1, Message="SUCCESS")

    except Exception as ex:
        message = f"Error occurred in readExcelFile: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)



# def readExcelFile(filePath: str) -> Result:
#     try:
#         pd.set_option("future.no_silent_downcasting", True)
#         # Step 1: Read raw Excel without headers to extract metadata
#         excelData = pd.read_excel(filePath, header=None)

#         # Step 2: Extract metadata
#         reportName = excelData.iloc[0, 1]
#         financialMonth = excelData.iloc[1, 1]

#         financialMonthNumber = datetime.strptime(financialMonth, "%B").month

#         # Step 3: Extract headers and data
#         headers = excelData.iloc[4]
#         data = excelData.iloc[5:].reset_index(drop=True)
#         data.columns = headers

#         # Optional conversion for consistency
#         data = data.applymap(
#             lambda x: x.item() if isinstance(x, (np.int64, np.float64)) else x
#         )

#         # Only return parsed data range as DateObjects
#         monthlyHeaderRow = data[data["Account Name"] == "Account Name"]

#         dataRangeFrame = monthlyHeaderRow.drop(
#             columns=["Classification", "Account Name"], errors="ignore"
#         )
#         dataRange = list(dataRangeFrame.columns)
#         dataRange = [m for m in dataRange if pd.notna(m)]

#         converted_data_range = [
#             DateObject(
#                 Month=(
#                     label.month
#                     if isinstance(label, datetime)
#                     else datetime.strptime(label, "%b %Y").month
#                 ),
#                 Year=(
#                     label.year
#                     if isinstance(label, datetime)
#                     else datetime.strptime(label, "%b %Y").year
#                 ),
#             )
#             for label in dataRange
#         ]


#         fileName = os.path.basename(filePath)

#         # converted_data_range = [
#         #     DateObject(
#         #         Month=datetime.strptime(label, "%b %Y").month,
#         #         # if monthAsString else datetime.strptime(label, "%b %Y").strftime("%b")),
#         #         Year=datetime.strptime(label, "%b %Y").year,
#         #     )
#         #     for label in dataRange
#         # ]
        
#         # <------------  Source Model Data Creation ----------------->
#         df_valid = excelData.dropna(subset=["Classification", "Account Name"], how="any")

#         # Total count (after filtering)
#         total_items = len(df_valid)

#         # Keep only rows with valid classification codes (e.g., REV, VCOS, FEXP)
#         df = df[df["Classification"].notna()]

#         # Group by Classification and create the list of Account Names
#         result = {
#             cls: [name for name in group["Account Name"].dropna().tolist()]
#             for cls, group in df.groupby("Classification")
#         }

#         sourceData = SourceMetaDataModel(SourceId=123456,SourceName=fileName,SourceType="Excel",FilePath=filePath,SheetName=list(excelData.keys())[0],TotalItems=total_items , ItemsList=result)

#         print(sourceData,'-----------------')


#         # <-------------------------------------------------------->

#         response = {
#             "Report Details": {
#                 "Company Name": reportName,
#                 "Financial Year": financialMonthNumber,
#                 "Data Range": converted_data_range,
#             },
#             "Financial Data": data,
#         }
#         return Result(Data=response, Status=1, Message="SUCCESS")
#     # return Result(Data=reportDescription, Status=1, Message="SUCCESS")

#     except Exception as ex:
#         message = f"Error occurred in extractExcelReportDetails: {ex}"
#         print(f"{datetime.now()} {message}")
#         return Result(Status=0, Message=message)
