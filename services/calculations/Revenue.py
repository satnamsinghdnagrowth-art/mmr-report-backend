from datetime import datetime
from typing import Optional
from core.models.base.ResultModel import Result
from helper.readExcel import readExcelFile
from helper.GetFileByReportId import getReportData
from helper.LoadJsonData import financialDataTest


# Get Total Revenue
def totalRevenue(year: int, month, reportId: Optional[int] = None):
    try:
        financialData = financialDataTest

        if reportId is not None:
            financialData = getReportData(reportId)

        data = financialData["PROFIT & LOSS"]["REVENUE"]["Total"]

        filteredData = [
            item for item in data if item["Month"] in month and item["Year"] == year
        ]

        if not filteredData:
            totalRevenue = 0

        totalRev = sum(item["Value"] for item in filteredData)

        return Result(
            Data=round(totalRev, 2),
            Status=1,
            Message="Month-wise calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at totalRevenue: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at totalRevenue: {ex}"
        # print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)


def revenueGrowth(year: int, month: list, reportId: Optional[int] = None):
    try:
        if not month or len(month) != 1:
            raise ValueError("Only one month should be provided in a list.")

        monthValue = month[0]

        # Calculate current month revenue
        thisMonthRevenue = totalRevenue(year, [monthValue], reportId).Data

        # Determine previous month and year
        if monthValue == 1:
            prevMonth = 12
            prevYear = year - 1
        else:
            prevMonth = monthValue - 1
            prevYear = year

        # Calculate previous month revenue
        prevMonthRevenue = totalRevenue(prevYear, [prevMonth], reportId).Data

        if prevMonthRevenue == 0:
            raise ZeroDivisionError(
                "Previous month revenue is zero, cannot calculate growth."
            )

        revGrowth = (
            (thisMonthRevenue - prevMonthRevenue) / abs(prevMonthRevenue)
        ) * 100

        return Result(
            Data=round(revGrowth, 2),
            Status=1,
            Message="Revenue growth calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at revenueGrowth: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occurred at revenueGrowth: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
