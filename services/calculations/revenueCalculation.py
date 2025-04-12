from datetime import datetime
from config.variable import variableMapping
from core.models.base.ResultModel import Result
from helper.readExcel import readExcelFile

def calculateRevenue():
    try:

        accountName = "REVENUE"

        filePath = "tempFiles/Honest Game Corporation Jan 2025 (4).xlsx"

        excelData = readExcelFile(filePath)

        data = excelData.Data
        
        revenueCode = variableMapping["PROFIT & LOSS"][accountName]

        revenueDF = data[data["Classification"].isin(revenueCode[0].keys())]

        month_cols = [
            col
            for col in revenueDF.columns
            if col not in ["Classification", "Account Name"]
        ]

        # Create a dictionary with total revenue for each month
        monthly_totals = {
            month: revenueDF[month].fillna(0).sum() for month in month_cols
        }

        # Return the monthly totals
        return Result(
            Data=monthly_totals,
            Status=1,
            Message="Month-wise revenue calculated successfully",
        )


    except Exception as ex:
        message = f"Error occur at calculateRevenue: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)

    