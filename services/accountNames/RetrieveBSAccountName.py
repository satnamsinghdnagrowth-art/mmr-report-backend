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

                next_month = 1 if month == 12 else month + 1
                next_month_year = year + 1 if month == 12 else year

                prev_month = 12 if month == 1 else month - 1
                prev_month_year = year - 1 if month == 1 else year

                monthly_totals = [
                    {
                        "Label": f"This Month - {getMonthName(month)} {year}",
                        "Month": [month],
                        "Year": year,
                    },
                    {
                        "Label": f"Next Month - {getMonthName(next_month)} {next_month_year}",
                        "Month": [next_month],
                        "Year": next_month_year,
                    },
                    {
                        "Label": f"Prev Month - {getMonthName(prev_month)} {prev_month_year}",
                        "Month": [prev_month],
                        "Year": prev_month_year,
                    },
                    {
                        "Label": f"This Year - {year}",
                        "Month": 0,
                        "Year": year,
                    },
                    {
                        "Label": f"Next Year - {year + 1}",
                        "Month": [0],
                        "Year": year + 1,
                    },
                    {
                        "Label": f"Prev Year - {year - 1}",
                        "Month": [0],
                        "Year": year - 1,
                    },
                    {
                        "Label": "This Quarter",
                        "Month": getQuarterMonthsFromMonth(month),
                        "Year": year,
                    },
                    {
                        "Label": "Prev Quarter",
                        "Month": getQuarterMonthsFromMonth(month - 3),
                        "Year": year,
                    },
                    {
                        "Label": "Next Quarter",
                        "Month": getQuarterMonthsFromMonth(month + 3),
                        "Year": year,
                    },
                    {
                        "Label": f"This Year ytd - {year}",
                        "Month": [1, 2, 3, 4],
                        "Year": year,
                    },
                    {
                        "Label": f"Next Year ytd - {year + 1}",
                        "Month": [1, 2, 3, 4],
                        "Year": year + 1,
                    },
                    {
                        "Label": f"Prev Year ytd - {year - 1}",
                        "Month": [1, 2, 3, 4],
                        "Year": year - 1,
                    },
                ]

                result[main][displayname] = monthly_totals

        return Result(Data=result, Status=1, Message="Success")

    except Exception as ex:
        message = f"Error occur at retriveBSAccountNames: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
