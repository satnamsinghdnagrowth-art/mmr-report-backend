from datetime import datetime
from core.models.base.ResultModel import Result
from helper.LoadJsonData import SECTION_CARD_CONFIGS
from core.models.visualsModel.ValueObject import ValueObjectModel
from services.calculations.DiffrenceCalculation import diffrenceAndPercentage
from core.models.visualsModel.TableModel import TableModel
from helper.LoadJsonData import financialDataTest
from config.FunctionMaping import functionRegistry
from helper.GetFileByReportId import getReportData
from helper.GetValueSymbol import getValueSymbol
from helper.metricCheck import isMetricPositive
from datetime import datetime


# Get the sections cards


def getTopOpeatingExpensesNew(
    year: int, months: list[int], reportType: str, section: str, reportId: int
):
    try:
        financialData = financialDataTest
        if reportId is not None:
            financialData = getReportData(reportId)["Financial Data"]

        configs = SECTION_CARD_CONFIGS.get(section)
        if not configs:
            return Result(
                Data=[],
                Status=1,
                Message=f"No tables configured for section '{section}'",
            )

        tables = []

        # Determine current month (assuming single month selected for "current")
        current_month = max(months) if months else 0
        # Generate last 6 months list in descending order (including current)
        prev_months = [(current_month - i - 1) % 12 or 12 for i in range(6)]
        prev_months = list(reversed(prev_months))  # oldest first

        # Header row
        headers = ["Expenses Names", "Total"] + [f"Month {m}" for m in prev_months]

        # Fetch all fixed expenses
        expensesdata = financialData["PROFIT & LOSS"]["EXPENSES"]["LineItems"][
            "Fixed Expenses"
        ].keys()
        expenses_with_totals = []

        # Step 1: Calculate total per expense
        for expenses in expensesdata:
            itemData = financialData["PROFIT & LOSS"]["EXPENSES"]["LineItems"][
                "Fixed Expenses"
            ][expenses]

            # Current period filter
            filterData = [
                item
                for item in itemData
                if (item["Year"] == year and (0 in months or item["Month"] in months))
            ]
            totalSum = sum(item["Value"] for item in filterData)

            # Collect last 6 month values
            month_values = []
            for m in prev_months:
                monthData = [
                    item["Value"]
                    for item in itemData
                    if item["Year"] == year and item["Month"] == m
                ]
                month_values.append(sum(monthData) if monthData else 0)

            expenses_with_totals.append((expenses, totalSum, month_values))

        # Step 2: Sort by total
        expenses_with_totals.sort(key=lambda x: x[1], reverse=True)

        # Step 3: Take top 10
        top_expenses = expenses_with_totals[:10]

        rows = []
        # Step 4: Format into ValueObjectModel rows
        for expense_name, totalSum, month_values in top_expenses:
            row = [
                ValueObjectModel(
                    Value=expense_name, isPositive=True, Type="", Symbol=""
                ),
                ValueObjectModel(
                    Value=totalSum, isPositive=True, Type="currency", Symbol="$"
                ),
            ]
            # Add last 6 month values
            for v in month_values:
                row.append(
                    ValueObjectModel(
                        Value=v, isPositive=True, Type="currency", Symbol="$"
                    )
                )
            rows.append(row)

        # Step 5: Wrap in table object
        tableObj = TableModel(
            Title="Top 10 Operating Expenses",
            Column=headers,
            Rows=rows,
        )
        tables.append(tableObj)

        return Result(
            Data=tableObj,
            Status=1,
            Message="Top 10 Operating Expenses calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at getTopOperatingExpenses: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
    except Exception as ex:
        message = f"Error occurred at getTopOperatingExpenses: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)


def getTopOpeatingExpenses(
    year: int, months: list[int], reportType: str, section: str, reportId: int
):
    try:
        financialData = financialDataTest
        if reportId is not None:
            financialData = getReportData(reportId)["Financial Data"]

        configs = SECTION_CARD_CONFIGS.get(section)

        if not configs:
            return Result(
                Data=[],
                Status=1,
                Message=f"No tables configured for section '{section}'",
            )

        tables = []
        Headers = ["Expenses Names", "Total"]

        expensesdata = financialData["PROFIT & LOSS"]["EXPENSES"]["LineItems"][
            "Fixed Expenses"
        ].keys()
        expenses_with_totals = []

        # Step 1: Calculate total per expense
        for expenses in expensesdata:
            itemData = financialData["PROFIT & LOSS"]["EXPENSES"]["LineItems"][
                "Fixed Expenses"
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
        top_expenses = expenses_with_totals[:10]

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
            Title="Top 10 Operating Expenses",
            Column=Headers,
            Rows=rows,
            TableType="Progress",
            Id="TOP_OPERATING_EXPENSES"
        )
        tables.append(tableObj)

        # tables.append(getTopOpeatingExpensesNew(year,months,reportType,section,reportId).Data)

        return Result(
            Data=tables,
            Status=1,
            Message="Top 10 Operating Expenses calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at getTopOperatingExpenses: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occurred at getTopOperatingExpenses: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
