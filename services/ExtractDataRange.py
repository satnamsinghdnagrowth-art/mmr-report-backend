import pandas as pd
from datetime import datetime
from core.models.Accounts.ReportDescriptionModel import (
    ReportDescriptionsModel,
    DateObject,
)

from core.models.base.ResultModel import Result


def retriveDataRange():
    try:
        filePath = "tempFiles/Honest Game Corporation Jan 2025 (4).xlsx"

        excelData = pd.read_excel(filePath, header=None)

        reportName = excelData.iloc[0, 1]
        financialYear = excelData.iloc[1, 1]

        excelData.columns = excelData.iloc[4]

        excelData = excelData.iloc[4:].reset_index(drop=True)

        monthlyHeaderRow = excelData[excelData["Account Name"] == "Account Name"]

        if monthlyHeaderRow.empty:
            return Result(Status=0, Message="No monthly header row found")

        dataRangeFrame = monthlyHeaderRow.drop(
            columns=["Classification", "Account Name"], errors="ignore"
        )

        # Get keys for the data range
        dataRange = list(dataRangeFrame.columns)

        converted_data_range = [
            DateObject(
                Month=datetime.strptime(label, "%b %Y").strftime("%B")[0:3],
                Year=datetime.strptime(label, "%b %Y").year,
            )
            for label in dataRange
        ]

        # Create response model
        reportDescription = ReportDescriptionsModel(
            ReportName=reportName,
            FinancialYear=financialYear,
            DataRange=converted_data_range,
        )

        return Result(Data=reportDescription, Status=1, Message="Success")

    except Exception as ex:
        message = f"Error occurred in retriveDataRange: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)


def retriveDataRangeTest():
    try:
        filePath = "tempFiles/Honest Game Corporation Jan 2025 (4).xlsx"

        excelData = pd.read_excel(filePath, header=None)

        reportName = excelData.iloc[0, 1]
        financialYear = excelData.iloc[1, 1]

        excelData.columns = excelData.iloc[4]

        excelData = excelData.iloc[4:].reset_index(drop=True)

        monthlyHeaderRow = excelData[excelData["Account Name"] == "Account Name"]

        if monthlyHeaderRow.empty:
            return Result(Status=0, Message="No monthly header row found")

        dataRangeFrame = monthlyHeaderRow.drop(
            columns=["Classification", "Account Name"], errors="ignore"
        )

        # Get keys for the data range
        dataRange = list(dataRangeFrame.columns)

        converted_data_range = [
            DateObject(
                Month=datetime.strptime(label, "%b %Y").month,
                Year=datetime.strptime(label, "%b %Y").year,
            )
            for label in dataRange
        ]

        # Create response model
        reportDescription = ReportDescriptionsModel(
            ReportName=reportName,
            FinancialYear=financialYear,
            DataRange=converted_data_range,
        )

        return Result(Data=reportDescription, Status=1, Message="Success")

    except Exception as ex:
        message = f"Error occurred in retriveDataRange: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
