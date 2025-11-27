from datetime import datetime
from typing import Optional
from core.models.base.ResultModel import Result
from services.calculations.Revenue import totalRevenue
from helper.LoadJsonData import financialDataTest
from typing import Optional
from helper.GetFileByReportId import getReportData
from services.calculations.OtherIncome import otherIncome
from core.models.base.SourceModel import SourceDataTypes
from helper.GetFinancialData import getFinancialData


# Get Direct Expenses (Total Cost of Sales)
def directExpenses(year: int, month, reportId: int, dataType: Optional[str] = SourceDataTypes.Actuals):
    try:
        financialData = getFinancialData(reportId, dataType)

        VCOSdata = financialData["PROFIT & LOSS"]["COST OF SALES"]["Classification"][
            "Variable Cost"
        ]

        VCOSFilter = [
            item
            for item in VCOSdata
            if (item["Year"] == year and (0 in month or item["Month"] in month))
        ]

        totalVCOS = sum(item["Value"] for item in VCOSFilter)

        FCOSdata = financialData["PROFIT & LOSS"]["COST OF SALES"]["Classification"][
            "Fixed Cost"
        ]

        FCOSFilter = [
            item
            for item in FCOSdata
            if (item["Year"] == year and (0 in month or item["Month"] in month))
        ]

        totalFCOS = sum(item["Value"] for item in FCOSFilter)

        totalDirectExpenses = totalFCOS + totalVCOS

        return Result(
            Data=round(totalDirectExpenses, 2),
            Status=1,
            Message="Month-wise DirectExpenses calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at directExpenses: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at directExpenses: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)


def interestExpenses(year: int, month, reportId: int, dataType: Optional[str] = SourceDataTypes.Actuals):
    try:
        financialData = getFinancialData(reportId, dataType)

        IEXPdata = financialData["PROFIT & LOSS"]["INTEREST EXPENSES"][
            "Classification"
        ]["Interest Expense"]

        IEXPFilter = [
            item
            for item in IEXPdata
            if (item["Year"] == year and (0 in month or item["Month"] in month))
        ]

        totalIEXP = sum(item["Value"] for item in IEXPFilter)

        return Result(
            Data=round(totalIEXP, 2),
            Status=1,
            Message="Month-wise interestExpenses calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at interestExpenses: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at interestExpenses: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)


# Get Total Operating Expenses (Operating Expenses)
def totalOperatingExpenses(year, month, reportId: int, dataType: Optional[str] = SourceDataTypes.Actuals):
    try:
        financialData = getFinancialData(reportId, dataType)

        FEXPdata = financialData["PROFIT & LOSS"]["EXPENSES"]["Classification"][
            "Variable Expenses"
        ]

        FEXPFilter = [
            item
            for item in FEXPdata
            if (item["Year"] == year and (0 in month or item["Month"] in month))
        ]

        totalFEXP = sum(item["Value"] for item in FEXPFilter)

        VEXPdata = financialData["PROFIT & LOSS"]["EXPENSES"]["Classification"][
            "Fixed Expenses"
        ]

        VEXPFilter = [
            item
            for item in VEXPdata
            if (item["Year"] == year and (0 in month or item["Month"] in month))
        ]

        totalVEXP = sum(item["Value"] for item in VEXPFilter)

        VEXPDA = financialData["PROFIT & LOSS"]["EXPENSES"]["Classification"][
            "Depreciation"
        ]

        DAFilter = [
            item
            for item in VEXPDA
            if (item["Year"] == year and (0 in month or item["Month"] in month))
        ]

        totalDA = sum(item["Value"] for item in DAFilter)

        totalOperatingExp = totalFEXP + totalVEXP + totalDA

        return Result(
            Data=round(totalOperatingExp, 2),
            Status=1,
            Message="Month-wise Total OperatingCost calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at totalOperatingExpenses: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at totalOperatingExpenses: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)


# Get Expenses To Revenue Ratio
def expensesToRevenueRatio(year: int, month, reportId: int, dataType: Optional[str] = SourceDataTypes.Actuals):
    try:
        operatingExp = totalOperatingExpenses(year, month, reportId).Data
        directExp = directExpenses(year, month, reportId).Data
        totalRev = totalRevenue(year, month, reportId).Data

        totalExpenses = operatingExp + directExp

        expToRevRation = (totalExpenses / totalRev) * 100

        return Result(
            Data=round(expToRevRation, 2),
            Status=1,
            Message="Expenses to Revenue Ratio calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at expensesToRevenueRatio: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at expensesToRevenueRation: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
