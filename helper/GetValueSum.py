from datetime import datetime
from typing import Optional, List
from core.models.base.ResultModel import Result


def getValueSum(
    financial_data: dict, path: List[str], year: int, months: List[int]
) -> float:
    """Fetch and filter data and return the total sum of values."""
    try:
        data = financial_data
        for key in path:
            data = data.get(key, {})
        totalValue = sum(
            item["Value"]
            for item in data
            if item["Year"] == year and (0 in months or item["Month"] in months)
        )

        if "Prepaid Expenses" in path:
            print(totalValue, year, months)

        return Result(
            Data=round(totalValue, 2),
            Status=1,
            Message="Total contribution calculated successfully",
        )

    except Exception as ex:
        message = f"Error occur at getValueSum: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
