from datetime import datetime
from config.variable import variableMapping
from core.models.base.ResultModel import Result
from helper.readExcel import readExcelFile
from helper.LoadJsonData import financialDataTest


# Get Total Revenue
def totalRevenue(year: int, month):
    try:
        data = financialDataTest["PROFIT & LOSS"]["REVENUE"]["Total"]

        filteredData = [
            item for item in data if item["Month"] in month and item["Year"] == year
        ]

        totalRevenue = filteredData[0]["Value"] if filteredData else 0

        return Result(
            Data=totalRevenue,
            Status=1,
            Message="Month-wise calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at totalRevenue: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at totalRevenue: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)


# Get Direct Expenses
def directExpenses(month, year: int):
    try:
        VCOSdata = financialDataTest["PROFIT & LOSS"]["COST OF SALES"][
            "Classification"
        ]["Variable Cost"]

        VCOSFilter = [
            item for item in VCOSdata if item["Month"] in month and item["Year"] == year
        ]

        totalVCOS = VCOSFilter[0]["Value"] if VCOSFilter else 0

        FCOSdata = financialDataTest["PROFIT & LOSS"]["COST OF SALES"][
            "Classification"
        ]["Fixed Cost"]

        FCOSFilter = [
            item for item in FCOSdata if item["Month"] == month and item["Year"] == year
        ]

        totalFCOS = FCOSFilter[0]["Value"] if FCOSFilter else 0

        totalDirectExpenses = totalFCOS + totalVCOS

        print(f"Revenue for {month}/{year}: {totalVCOS},{totalFCOS}")

        return Result(
            Data=totalDirectExpenses,
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


# Get Gross Profit
def grossProfit(year: int, month):
    try:
        totalRev = totalRevenue(year, month).Data
        grossProfit = totalRev - directExpenses(month, year).Data

        return Result(
            Data=grossProfit,
            Status=1,
            Message="Gross Profit calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at grossProfit: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at grossProfit: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)


# Get Gross Profit Margin
def grossProfitMargin(year: int, month):
    try:
        totalRev = totalRevenue(year, month).Data
        GP = grossProfit(year, month).Data
        GPM = GP / totalRev

        return Result(
            Data=GPM,
            Status=1,
            Message="Gross Profit calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at grossProfitMargin: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at totalRevenue: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)


# Get Total Operating Expenses
def totalOperatingExpenses(month, year: int):
    try:
        FEXPdata = financialDataTest["PROFIT & LOSS"]["EXPENSES"]["Classification"][
            "Variable Expenses"
        ]

        FEXPFilter = [
            item for item in FEXPdata if item["Month"] in month and item["Year"] == year
        ]

        totalFEXP = FEXPFilter[0]["Value"] if FEXPFilter else 0

        VEXPdata = financialDataTest["PROFIT & LOSS"]["EXPENSES"]["Classification"][
            "Fixed Expenses"
        ]

        VEXPFilter = [
            item for item in VEXPdata if item["Month"] in month and item["Year"] == year
        ]

        totalVEXP = VEXPFilter[0]["Value"] if VEXPFilter else 0

        VEXPDA = financialDataTest["PROFIT & LOSS"]["EXPENSES"]["Classification"][
            "Depreciation"
        ]

        DAFilter = [
            item for item in VEXPDA if item["Month"] in month and item["Year"] == year
        ]

        totalDA = DAFilter[0]["Value"] if DAFilter else 0

        totalOperatingCost = totalFEXP + totalVEXP + totalDA

        print(f"Revenue for {month}/{year}: {totalOperatingCost}")

        return Result(
            Data=totalOperatingCost,
            Status=1,
            Message="Month-wise Total OperatingCost calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at totalOperatingExpenses: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at totalRevenue: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)


# Get EBIT
def EBIT(year: int, month):
    try:
        GP = grossProfit(year, month).Data

        operatingCost = totalOperatingExpenses(month, year).Data

        print(f"GP:{grossProfit},operatingEXp:{operatingCost}")

        totalEBIT = GP - operatingCost

        return Result(
            Data=totalEBIT,
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


# Get EBIT Margin
def EBITMargin(year: int, month):
    try:
        totalRev = totalRevenue(year, month).Data
        totalEBIT = EBIT(year, month).Data

        ebitMargin = totalEBIT / totalRev

        return Result(
            Data=ebitMargin,
            Status=1,
            Message="EBIT Margin calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at EBITMargin: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=0, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occur at totalRevenue: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)


# Get Expenses To Revenue Ratio
def expensesToRevenueRatio(year: int, month):
    try:
        operatingExp = totalOperatingExpenses(month, year).Data
        directExp = directExpenses(month, year).Data
        totalRev = totalRevenue(year, month).Data

        totalExpenses = operatingExp + directExp

        print(f"OE:{operatingExp},DE:{directExp},TR:{totalRev}")

        expToRevRation = totalExpenses / totalRev

        return Result(
            Data=expToRevRation,
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
