from datetime import datetime
from config.variable import variableMapping
from core.models.base.ResultModel import Result
from services.calculations.Ebit import EBIT
from typing import Optional,List
from services.calculations.OtherIncome import otherIncome, interestIncome
from helper.LoadJsonData import financialDataTest
from core.models.base.SourceModel import SourceDataTypes
from helper.GetFileByReportId import getReportData
from helper.GetFinancialData import getFinancialData



# Operating Profit
def earningBeforeInterestandTax(year: int, month: List[int], reportId: int,dataType: Optional[str] = SourceDataTypes.Actuals):
    try:
        ebit = EBIT(year, month, reportId).Data

        otherIC = otherIncome(year, month, reportId).Data

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


def earningBeforeTax(year: int, month : List[int], reportId: int,dataType: Optional[str] = SourceDataTypes.Actuals):
    try:
        financialData = getFinancialData(reportId, dataType)
        ebit = EBIT(year, month, reportId).Data

        interestIC = interestIncome(year, month, reportId).Data

        TEXPdata = financialData["PROFIT & LOSS"]["INTEREST EXPENSES"][
            "Classification"
        ]["Interest Expense"]

        TEXPFilter = [
            item
            for item in TEXPdata
            if (item["Year"] == year and (0 in month or item["Month"] in month))
        ]

        totalIEXP = sum(item["Value"] for item in TEXPFilter)

        if month == [1, 2, 3, 4, 5, 6, 7]:
            print(totalIEXP, "99845495948654")

            print(totalIEXP)

        # otherIncomeValue = otherIncome(year, month,reportId).Data

        result = (ebit + interestIC) - totalIEXP

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
