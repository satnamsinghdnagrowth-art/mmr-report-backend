from datetime import datetime
from helper.getMonthName import getMonthName
from collections import defaultdict
from config.variable import variableMapping
from core.models.base.ResultModel import Result


# Analyze the data
def retriveBSAccountNames(category: str, month=4, year=2023):
    try:
        result = defaultdict(dict)

        BSData = variableMapping[category]

        for main, category in BSData.items():
            for code in category:
                displayname = list(code.values())[0]

                monthly_totals = [
                    {
                        "Label": f"This Month-{getMonthName(month)} {year}",
                        "Month": month,
                        "Year": year,
                    },
                    {
                        "Label": f"This Month-{getMonthName(month + 1)} {year}",
                        "Month": month + 1,
                        "Year": year,
                    },
                    {
                        "Label": f"This Month-{getMonthName(month - 1)} {year}",
                        "Month": month - 1,
                        "Year": year,
                    },
                    {"Label": f"This Year-{year}", "Month": 0, "Year": year},
                    {"Label": f"Next Year-{year + 1}", "Month": 0, "Year": year + 1},
                    {"Label": f"Prev Year {year - 1}", "Month": 0, "Year": year - 1},
                ]

                result[main][displayname] = monthly_totals

        return Result(Data=result, Status=1, Message="Success")

    except Exception as ex:
        message = f"Error occur at retriveBSAccountNames: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
