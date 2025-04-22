from datetime import datetime
from helper.getMonthName import getMonthName
from services.calculations.revenueCalculation import calculateRevenue
from core.models.base.ResultModel import Result


def retriveKPIsNames(month :int,year :int):
    try:
        # resultDict = {"PROFITIABILITY": {"TotalRevenue": calculateRevenue().Data}}

        monthly_totals = [
            {
                "Label": f"This Month-{getMonthName(month)} {year}",
                "Month": month,
                "Year": year,
            },
            {
                "Label": f"Next Month-{getMonthName(month + 1)} {year}",
                "Month": month + 1,
                "Year": year,
            },
            {
                "Label": f"Prev Month-{getMonthName(month - 1)} {year}",
                "Month": month - 1,
                "Year": year,
            },
            {"Label": f"This Year-{year}", "Month": 0, "Year": year},
            {"Label": f"Next Year-{year + 1}", "Month": 0, "Year": year + 1},
            {"Label": f"Prev Year {year - 1}", "Month": 0, "Year": year - 1},
        ]


        resultDict = {"PROFITIABILITY": {"TotalRevenue": monthly_totals}}

        return Result(
            Data=resultDict,
            Status=1,
            Message="KPIs Name retrieve Succesfully",
        )

    except Exception as ex:
        message = f"Error occur at retriveKPIsNames: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
