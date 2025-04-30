from datetime import datetime
from core.models.base.ResultModel import Result
from services.calculations.Ebit import EBIT
from services.calculations.Revenue import totalRevenue
from helper.LoadJsonData import financialDataTest


# Get Total Revenue
def otherIncome(year: int, month):
    try:

        

        # Another Expenses
        AINCdata = financialDataTest["PROFIT & LOSS"]["OTHER INCOME"]["Classification"][
            "Additional Income"
        ]

        AINCFilter = [
            item for item in AINCdata
            if (item["Year"] == year and (0 in month or item["Month"] in month))
        ]

        totalAINC = sum(item["Value"] for item in AINCFilter)

        otherIncome = 0 + totalAINC 

        return Result(
            Data=round(otherIncome,2),
            Status=1,
            Message="otherIncome calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at otherIncome: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at otherIncome: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
    



#  Get Total Revenue
def interestIncome(year: int, month):
    try:
        # Interest Expenses
        interestIncomedata = financialDataTest["PROFIT & LOSS"]["OTHER INCOME"]["Classification"][
            "Investment Income"
        ]

        IINCFilter = [
            item for item in interestIncomedata
            if (item["Year"] == year and (0 in month or item["Month"] in month))
        ]

        totalIINC = sum(item["Value"] for item in IINCFilter)


        return Result(
            Data=round(totalIINC,2),
            Status=1,
            Message="NetProfit Margin calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at otherIncomeMargin: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at otherIncomeMargin: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)

