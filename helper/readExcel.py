import pandas as pd
import numpy as np
import os, json
from datetime import datetime
from core.models.base.ResultModel import Result
from core.models.Accounts.ReportDescriptionModel import DateObject
from core.models.base.SourceModel import SourceMetaDataModel
from config.FilesBaseDIR import SOURCE_JSON_PATH


# def readExcelFile(filePath: str, reportId: int) -> Result:
#     try:
#         pd.set_option("future.no_silent_downcasting", True)

#         # Step 1: Read Excel with sheet names
#         excelData = pd.read_excel(filePath, header=None, sheet_name=None)
#         sheetName = list(excelData.keys())[0]
#         sheetData = excelData[sheetName]

#         # Step 2: Extract metadata safely
#         reportName = str(sheetData.iloc[0, 1]) if not pd.isna(sheetData.iloc[0, 1]) else "Unknown Report"
#         financialMonth = str(sheetData.iloc[1, 1]) if not pd.isna(sheetData.iloc[1, 1]) else "January"

#         try:
#             financialMonthNumber = datetime.strptime(financialMonth, "%B").month
#         except ValueError:
#             financialMonthNumber = 1  # Default to January if parsing fails

#         # Step 3: Extract headers and data
#         headers = sheetData.iloc[4].tolist()
#         data = sheetData.iloc[5:].reset_index(drop=True)
#         data.columns = headers

#         # Clean and normalize values
#         data = data.map(
#             lambda x: x.item() if isinstance(x, (np.int64, np.float64)) else x
#         )

#         # Step 4: Extract date range
#         monthlyHeaderRow = data[data["Account Name"] == "Account Name"]
#         if not monthlyHeaderRow.empty:
#             dataRangeFrame = monthlyHeaderRow.drop(
#                 columns=["Classification", "Account Name"], errors="ignore"
#             )
#             dataRange = [m for m in dataRangeFrame.columns if pd.notna(m)]
#         else:
#             dataRange = []

#         converted_data_range = [
#             DateObject(
#                 Month=datetime.strptime(label, "%b %Y").month,
#                 # if monthAsString else datetime.strptime(label, "%b %Y").strftime("%b")),
#                 Year=datetime.strptime(label, "%b %Y").year,
#             )
#             for label in dataRange
#         ]

#         fileName = os.path.basename(filePath)

#         # Step 5: Filter valid rows (both Classification and Account Name not empty)
#         df_valid = data.dropna(subset=["Classification", "Account Name"], how="any")

#         # Total count of valid rows
#         total_items = len(df_valid)

#         # Step 6: Group by Classification and make list of Account Names
#         grouped = {
#             cls: group["Account Name"].dropna().tolist()
#             for cls, group in df_valid.groupby("Classification")
#         }

#         # Convert dict to list of dicts for Pydantic validation
#         items_list = [{key: value} for key, value in grouped.items()]

#         # Step 7: Create source metadata model
#         sourceData = SourceMetaDataModel(
#             SourceId=int(datetime.now().timestamp()),
#             ReportId=reportId,
#             SourceName=fileName,
#             SourceType="Excel",
#             FilePath=filePath,
#             SheetName=sheetName,
#             TotalItems=total_items,
#             ItemsList=items_list,
#         )

#         # Step 8: Build final response
#         response = {
#             "Report Details": {
#                 "Company Name": reportName,
#                 "Financial Year": financialMonthNumber,
#                 "Data Range": converted_data_range,
#             },
#             "Financial Data": data,
#         }

#         # Step 9: Save metadata JSON safely
#         os.makedirs(os.path.dirname(SOURCE_JSON_PATH), exist_ok=True)

#         if os.path.exists(SOURCE_JSON_PATH) and os.path.getsize(SOURCE_JSON_PATH) > 0:
#             with open(SOURCE_JSON_PATH, "r") as f:
#                 try:
#                     existing_data = json.load(f)
#                     if not isinstance(existing_data, list):
#                         existing_data = []
#                 except json.JSONDecodeError:
#                     existing_data = []
#         else:
#             existing_data = []

#         existing_data.append(sourceData.model_dump())

#         with open(SOURCE_JSON_PATH, "w") as f:
#             json.dump(existing_data, f, indent=4, default=str)

#         # Step 10: Return result
#         return Result(Data=response, Status=1, Message="SUCCESS")

#     except Exception as ex:
#         message = f"Error occurred in readExcelFile: {ex}"
#         print(f"{datetime.now()} {message}")
#         return Result(Status=0, Message=message)


def readExcelFile(filePath: str, reportId: int) -> Result:
    try:
        pd.set_option("future.no_silent_downcasting", True)

        # Step 1: Read raw Excel without headers to extract metadata
        excelData = pd.read_excel(filePath, header=None)

        # Step 2: Extract metadata
        reportName = excelData.iloc[0, 1]
        financialMonth = excelData.iloc[1, 1]
        financialMonthNumber = datetime.strptime(financialMonth, "%B").month

        # Step 3: Extract headers and data
        headers = excelData.iloc[4]
        data = excelData.iloc[5:].reset_index(drop=True)
        data.columns = headers

        # Optional conversion for consistency
        data = data.map(
            lambda x: x.item() if isinstance(x, (np.int64, np.float64)) else x
        )

        # Step 4: Extract data range
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
            ).dict()
            for label in dataRange
        ]

        fileName = os.path.basename(filePath)

        # ✅ <------------  Source Model Data Creation ----------------->
        if "Classification" not in data.columns or "Account Name" not in data.columns:
            raise ValueError(
                "Excel must contain 'Classification' and 'Account Name' columns."
            )

        # Filter valid rows
        df_valid = data.dropna(subset=["Classification", "Account Name"], how="any")

        # Total count
        total_items = len(df_valid)

        # Group by Classification
        result = {
            cls: [name for name in group["Account Name"].dropna().tolist()]
            for cls, group in df_valid.groupby("Classification")
        }

        # Extract first sheet name
        sheetName = pd.ExcelFile(filePath).sheet_names[0]

        sourceData = SourceMetaDataModel(
            SourceId=123456,
            ReportId=reportId,
            SourceName=fileName,
            SourceType="Excel",
            FilePath=filePath,
            SheetName=sheetName,
            TotalItems=total_items,
            ItemsList=[{"Classification": k, "Accounts": v} for k, v in result.items()],
            CreatedOn=datetime.now(),
            UpdatedOn=datetime.now(),
        )

        existing_data = []

        os.makedirs(os.path.dirname(SOURCE_JSON_PATH), exist_ok=True)

        if os.path.exists(SOURCE_JSON_PATH) and os.path.getsize(SOURCE_JSON_PATH) > 0:
            with open(SOURCE_JSON_PATH, "r") as f:
                try:
                    existing_data = json.load(f)
                    if not isinstance(existing_data, list):
                        existing_data = []
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []

        existing_data.append(sourceData.model_dump())

        with open(SOURCE_JSON_PATH, "w") as f:
            json.dump(existing_data, f, indent=4, default=str)

        response = {
            "Report Details": {
                "Company Name": reportName,
                "Financial Year": financialMonthNumber,
                "Data Range": converted_data_range,
            },
            "Financial Data": data,
            "Source Meta": sourceData.dict(),
        }
        return Result(Data=response, Status=1, Message="SUCCESS")

    except Exception as ex:
        message = f"Error occurred in readExcelFile: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
