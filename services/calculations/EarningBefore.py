from datetime import datetime
from config.variable import variableMapping
from core.models.base.ResultModel import Result
from services.calculations.Ebit import EBIT
from typing import Optional
from services.calculations.OtherIncome import otherIncome, interestIncome
from helper.LoadJsonData import financialDataTest
from helper.GetFileByReportId import getReportData


# Operating Profit
def earningBeforeInterestandTax(year: int, month,reportId:Optional[int]=None):
    try:

        ebit = EBIT(year, month,reportId).Data

        otherIC = otherIncome(year, month,reportId).Data

        result = ebit + otherIC

        return Result(
            Data=round(result, 2),
            Status=1,
            Message="Total EBIT calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at earningBeforeInterestandTax: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at earningBeforeInterestandTax: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)


def earningBeforeTax(year: int, month,reportId:Optional[int]=None):
    try:
        ebit = earningBeforeInterestandTax(year, month,reportId).Data

        interestIC = interestIncome(year, month,reportId).Data

        result = ebit + interestIC

        return Result(
            Data=round(result, 2),
            Status=1,
            Message="Total EBIT calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at earningBeforeInterestandTax: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at earningBeforeInterestandTax: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
