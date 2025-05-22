import pandas as pd
from datetime import datetime
from core.models.Accounts.ReportDescriptionModel import (
    ReportDescriptionsModel,
    DateObject,
)
from helper.readExcel import readExcelFile
from core.models.base.ResultModel import Result

from helper.GetFileByReportId import getReportData

       


def retriveDataRange():

    try:

        # financialData = getReportData(reportId) if reportId else financialData
        filePath = "tempFiles/Honest Game Corporation Jan 2025 (4).xlsx"

        excelData = pd.read_excel(filePath, header=None)

        data = readExcelFile(filePath).Data

        reportDetails = data["Report Details"]

        companyName = reportDetails["Company Name"]

        finacialYear = reportDetails["Financial Year"]

        dateRange = reportDetails["Data Range"]

        # # Create response model
        reportDescription = ReportDescriptionsModel(
            ReportName=companyName,
            FinancialYear=finacialYear,
            DataRange=dateRange,
        )

        return Result(Data=reportDescription, Status=1, Message="Success")

    except Exception as ex:
        message = f"Error occurred in retriveDataRange: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)

