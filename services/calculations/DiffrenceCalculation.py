from datetime import datetime
from core.models.base.ResultModel import Result
from typing import Optional
# Helper function to calculate differences and percentage change


def diffrenceAndPercentage(this_month_value, prev_month_value):
    try:
        diff = this_month_value - prev_month_value
        percentChange = 0
        if prev_month_value != 0:
            percentChange = round((diff / abs(prev_month_value)) * 100, 2)
        resultData = {"Diffrence": round(diff, 2), "PercentChange": percentChange}

        return Result(
            Data=resultData,
            Status=1,
            Message="Total EBIT calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at EBIT: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at totalRevenue: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
