from datetime import datetime
from services.accountNames.RetrieveCOANames import retriveCOANames
from services.accountNames.RetrieveBSAccountName import retriveBSAccountNames
from services.accountNames.RetrieveKPIsNames import retriveKPIsNames
from core.models.base.ResultModel import Result
from services.calculations.RevenueCalculation import (
    expensesToRevenueRatio,
    EBITMargin,
    totalRevenue,
    grossProfit,
    grossProfitMargin,
    EBIT,
)


# Analyze the data
def retreiveKPIsValue(section, subSection, month, year: int):
    try:
        value = 0
        if subSection == "TotalRevenue":
            value = totalRevenue(year, month).Data

        if subSection == "Gross Profit":
            value = grossProfit(year, month).Data
            print(value)

        if subSection == "Gross Profit Margin":
            value = grossProfitMargin(year, month).Data

        if subSection == "EBIT":
            value = EBIT(year, month).Data

        if subSection == "EBIT Margin":
            value = EBITMargin(year, month).Data

        if subSection == "Expenses To Revenue Ration":
            value = expensesToRevenueRatio(year, month).Data
            print(value, "fdgbfdbgj")

        return Result(Data=value, Status=1, Message="Success")

    except Exception as ex:
        message = f"Error occur at retreiveNames: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
