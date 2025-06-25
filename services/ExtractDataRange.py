import pandas as pd
from datetime import datetime
from core.models.Accounts.ReportDescriptionModel import (
    ReportDescriptionsModel,
    DateObject,
)
from helper.readExcel import readExcelFile
from typing import Optional
from core.models.base.ResultModel import Result
from helper.GetFileByReportId import getReportData
from helper.GetFileByReportId import getReportMetaDatabyId

def retriveDataRange(reportId:Optional[int]=None):
    try:

        reportData = getReportData(reportId)

        companyLogoPath = getReportMetaDatabyId(reportId).get("CompanyLogoFilePath")

        print(getReportMetaDatabyId(reportId),getReportMetaDatabyId(reportId).get("CompanyLogoFilePath"))

        reportDetails = reportData["Report Details"]

        companyName = reportDetails["Company Name"]

        finacialYear = reportDetails["Financial Year"]

        dateRange = reportDetails["Data Range"]

        # # Create response model
        reportDescription = ReportDescriptionsModel(
            ReportName=companyName,
            FinancialYear=finacialYear,
            DataRange=dateRange,
            CompanyLogoPath=companyLogoPath

        )

        return Result(Data=reportDescription, Status=1, Message="Success")

    except Exception as ex:
        message = f"Error occurred in retriveDataRange: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)

