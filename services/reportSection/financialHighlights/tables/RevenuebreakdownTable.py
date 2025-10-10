from datetime import datetime
from core.models.base.ResultModel import Result
from helper.LoadJsonData import SECTION_CARD_CONFIGS
from core.models.visualsModel.TableModel import TableModel, TableTypesName
from core.models.visualsModel.ChartModel import ChartDataModel, YAxisSeriesModel
from helper.LoadJsonData import financialDataTest
from helper.GetFileByReportId import getReportData
from core.models.visualsModel.ValueObject import ValueObjectModel
from helper.GetValueSymbol import getValueSymbol
from services.calculations.DiffrenceCalculation import diffrenceAndPercentage
from config.FunctionMaping import functionRegistry
from datetime import datetime
from typing import List
from services.reportSection.financialHighlights.tables.RevenueBreakDown import (
    getRevenueTable,
)


# Get the sections cards
def getRevenueBreakdownTable(year: int, months: list[int], section: str, reportId: int):
    try:
        financialData = financialDataTest
        if reportId is not None:
            financialData = getReportData(reportId)["Financial Data"]

        configs = SECTION_CARD_CONFIGS.get(section)

        tables = []
        Headers = ["Revenue Channels", "Total"]

        expensesdata = financialData["PROFIT & LOSS"]["REVENUE"]["LineItems"][
            "Revenue"
        ].keys()
        expenses_with_totals = []

        # Step 1: Calculate total per expense
        for expenses in expensesdata:
            itemData = financialData["PROFIT & LOSS"]["REVENUE"]["LineItems"][
                "Revenue"
            ][expenses]

            filterData = [
                item
                for item in itemData
                if (item["Year"] == year and (0 in months or item["Month"] in months))
            ]

            totalSum = sum(item["Value"] for item in filterData)
            expenses_with_totals.append((expenses, totalSum))

        # Step 2: Sort expenses by total in descending order
        expenses_with_totals.sort(key=lambda x: x[1], reverse=True)

        # Step 3: Take top 10 expenses
        top_expenses = expenses_with_totals

        rows = []

        # Step 4: Format into ValueObjectModel rows
        for expense_name, totalSum in top_expenses:
            row = [
                ValueObjectModel(
                    Value=expense_name,
                    isPositive=True,
                    Type="",
                    Symbol="",
                ),
                ValueObjectModel(
                    Value=totalSum,
                    isPositive=True,
                    Type="currency",
                    Symbol="$",
                ),
            ]
            rows.append(row)

        # Step 5: Wrap in table object
        tableObj = TableModel(
            Title="Revenue Breakdown",
            Column=Headers,
            Rows=rows,
            TableType=TableTypesName.Progress.value,
        )

        # tables.append(getTopOpeatingExpensesNew(year,months,reportType,section,reportId).Data)

        return Result(
            Data=tableObj,
            Status=1,
            Message="Revenue BreakDown calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at getRevenueBreakdownChart: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occurred at getRevenueBreakdownChart: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
