from datetime import datetime
from helper.getMonthName import getMonthName
from collections import defaultdict
from config.variable import variableMapping
from helper.getMonthName import getQuarterMonthsFromMonth
from core.models.base.ResultModel import Result


# Analyze the data
def retriveBSAccountNames(year, month, category: str):
    try:
        result = defaultdict(dict)

        BSData = variableMapping[category]

        for main, category in BSData.items():
            for code in category:
                displayname = list(code.values())[0]

                monthly_totals = [
                    {
                        "Label": f"This Month-{getMonthName(month)} {year}",
                        "Month": [month],  # Only the current month
                        "Year": year,
                    },
                    {
                        "Label": f"Next Month-{getMonthName(month + 1)} {year}",
                        "Month": [month + 1],  # Only the next month
                        "Year": year,
                    },
                    {
                        "Label": f"Prev Month-{getMonthName(month - 1)} {year}",
                        "Month": [month - 1],  # Only the previous month
                        "Year": year,
                    },
                    {
                        "Label": f"This Year-{year}",
                        "Month": 0,
                        "Year": year,
                    },  # All months in the current year
                    {
                        "Label": f"Next Year-{year + 1}",
                        "Month": [0],  # All months in the next year
                        "Year": year + 1,
                    },
                    {
                        "Label": f"Prev Year {year - 1}",
                        "Month": [0],  # All months in the previous year
                        "Year": year - 1,
                    },
                    {
                        "Label": f"This Quarter",
                        "Month": getQuarterMonthsFromMonth(month),  # All months in Q1
                        "Year": year,
                    },
                    {
                        "Label": f"Prev Quarter",
                        "Month": getQuarterMonthsFromMonth(
                            month - 3
                        ),  # All months in Q2
                        "Year": year,
                    },
                    {
                        "Label": f"Next Quarter",
                        "Month": getQuarterMonthsFromMonth(
                            month + 3
                        ),  # All months in Q3
                        "Year": year,
                    },
                    {
                        "Label": f"This Year YTD-{year}",
                        "Month": [1, 2, 3, 4],
                        "Year": year,
                    },  # All months in the current year
                    {
                        "Label": f"Next Year- YTD{year + 1}",
                        "Month": [1, 2, 3, 4],  # All months in the next year
                        "Year": year + 1,
                    },
                    {
                        "Label": f"Prev Year YTD{year - 1}",
                        "Month": [1, 2, 3, 4],  # All months in the previous year
                        "Year": year - 1,
                    },
                ]

                result[main][displayname] = monthly_totals

        return Result(Data=result, Status=1, Message="Success")

    except Exception as ex:
        message = f"Error occur at retriveBSAccountNames: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
