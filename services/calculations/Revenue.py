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
            financialData = getReportData(reportId)["Financial Data"]

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


from typing import Optional, List
from datetime import datetime


def revenueGrowth(year: int, month: List[int], reportId: Optional[int] = None):
    try:
        if not month:
            raise ValueError("Month list cannot be empty.")

        # Define quarter mapping
        quarter_map = {
            1: [1, 2, 3],
            2: [4, 5, 6],
            3: [7, 8, 9],
            4: [10, 11, 12],
        }

        # Determine if user passed full quarter or single month
        if len(month) > 1:
            # Find current quarter
            current_quarter = next(
                q for q, m in quarter_map.items() if set(month).issubset(set(m))
            )

            # Determine previous quarter and year
            if current_quarter == 1:
                prev_quarter = 4
                prev_year = year - 1
            else:
                prev_quarter = current_quarter - 1
                prev_year = year

            current_months = quarter_map[current_quarter]
            prev_months = quarter_map[prev_quarter]

            mode = "quarter"

        else:
            # Single month growth
            month_value = month[0]

            if month_value == 1:
                prev_month = 12
                prev_year = year - 1
            else:
                prev_month = month_value - 1
                prev_year = year

            current_months = [month_value]
            prev_months = [prev_month]

            mode = "month"

        # Calculate revenues
        this_period_revenue = totalRevenue(year, current_months, reportId).Data
        prev_period_revenue = totalRevenue(prev_year, prev_months, reportId).Data

        if prev_period_revenue == 0:
            raise ZeroDivisionError(
                "Previous period revenue is zero, cannot calculate growth."
            )

        rev_growth = (
            (this_period_revenue - prev_period_revenue) / abs(prev_period_revenue)
        ) * 100

        return Result(
            Data=round(rev_growth, 2),
            Status=1,
            Message=f"Revenue growth calculated successfully for {mode}.",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at revenueGrowth: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occurred at revenueGrowth: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
