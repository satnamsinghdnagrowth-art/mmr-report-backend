from datetime import datetime
from config.variable import variableMapping
from core.models.base.ResultModel import Result
from services.calculations.Ebit import EBIT
from services.calculations.OtherIncome import otherIncome,interestIncome
from helper.LoadJsonData import financialDataTest

# Operating Profit
def earningBeforeInterestandTax(year: int, month):
    try:
        ebit = EBIT(year,month).Data

        otherIC = otherIncome(year,month).Data

        result = ebit+otherIC

        return Result(
            Data=round(result,2),
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
    

def earningBeforeTax(year: int, month):
    try:
        ebit = earningBeforeInterestandTax(year,month).Data

        interestIC = interestIncome(year,month).Data

        print(ebit,interestIC)

        result = ebit + interestIC

        return Result(
            Data=round(result,2),
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
