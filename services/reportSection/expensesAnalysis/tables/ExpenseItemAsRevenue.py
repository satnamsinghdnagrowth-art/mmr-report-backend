from datetime import datetime
from core.models.base.ResultModel import Result
from helper.LoadJsonData import SECTION_CARD_CONFIGS
from core.models.visualsModel.ValueObject import ValueObjectModel
from core.models.visualsModel.TableModel import TableModel
from helper.LoadJsonData import financialDataTest
from helper.GetFileByReportId import getReportData
import calendar


def expenseItemAsRevenueTable(
    year: int, months: list[int], section: str, reportId: int
):
    try:
        monthsList = range(1, months[-1] + 1)

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
        Headers = [f"{calendar.month_abbr[m]}" for m in monthsList]

        expensesdata = financialData["PROFIT & LOSS"]["EXPENSES"]["LineItems"][
            "Fixed Expenses"
        ].keys()

        expenses_with_totals = []

        # Step 1: Calculate monthly + total per expense
        for expense in expensesdata:
            itemData = financialData["PROFIT & LOSS"]["EXPENSES"]["LineItems"][
                "Fixed Expenses"
            ][expense]

            expensesMonthly = []
            total_all_months = 0

            for m in monthsList:
                filterData = [
                    item
                    for item in itemData
                    if (item["Year"] == year and item["Month"] == m)
                ]

                totalSum = sum(item["Value"] for item in filterData)
                total_all_months += totalSum
                expensesMonthly.append((expense, totalSum))

            expenses_with_totals.append((expense, expensesMonthly, total_all_months))

        # Step 2: Sort expenses by grand total in descending order
        expenses_with_totals.sort(key=lambda x: x[2], reverse=True)

        # Step 3: Take top 10 expenses
        top_expenses = expenses_with_totals[:10]
   rows = []

        # Step 4: Format into ValueObjectModel rows
        for expense_name, monthly_data, _ in top_expenses:
            row = [
                ValueObjectModel(
                    Value=expense_name,
                    isPositive=True,
                    Type="",
                    Symbol="",
                )
            ]

            for _, totalSum in monthly_data:
                row.append(
                    ValueObjectModel(
                        Value=totalSum,
                        isPositive=True,
                        Type="currency",
                        Symbol="$",
                    )
                )

            rows.append(row)

        # Step 5: Wrap in table object
        tableObj = TableModel(
            Title="Top 10 Operating Expenses", Column=Headers, Rows=rows
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
