from datetime import datetime
from typing import Optional, List
from core.models.base.ResultModel import Result
from core.models.base.SourceModel import SourceDataTypes
from helper.GetFinancialData import getFinancialData
from core.models.base.SourceModel import SourceDataTypes
from helper.GetCurrentPrevPeriods import getCurrentAndPreviousPeriods
from core.models.visualsModel.ValueObject import ValueObjectModel
from helper.GetValueSymbol import getValueSymbol
from helper.metricCheck import isMetricPositive
from datetime import datetime
from typing import Optional, List, Any
from core.models.base.ResultModel import Result
from core.models.base.SourceModel import SourceDataTypes
from helper.GetFinancialData import getFinancialData
from helper.GetCurrentPrevPeriods import getCurrentAndPreviousPeriods
from core.models.visualsModel.TableModel import TableModel, TableListModel
import calendar


def get_total(values, year, months):
    """Sum all values for given year + months list."""
    return sum(
        item["Value"]
        for item in values
        if item["Year"] == year and (item["Month"] in months or 0 in months)
    )

def varianceTable(year: int, month: List[int], reportId, dataType: Optional[str] = SourceDataTypes.Actuals):
    try:
        print(year, month, reportId)

        currentYear, currentMonths, prevYear, prevMonths = getCurrentAndPreviousPeriods(
            year, month, "Month"
        )

        # ----------- COLUMNS ------------
        columns = [
            "Item",
            f"{calendar.month_abbr[currentMonths[0]]} {year}",
            f"{calendar.month_abbr[prevMonths[0]]} {year}",
            "Budget (This Month)",
            "This Month vs Budget ($)",
            "This Month vs Last Month ($)",
            f"{year} (YTD)",
            "Budget (YTD)",
        ]

        # ----------- LOAD DATA ------------
        actualData = getFinancialData(reportId, dataType)
        actualLineItems = actualData["PROFIT & LOSS"]["REVENUE"]["LineItems"]["Revenue"]

        budgetData = getFinancialData(reportId, SourceDataTypes.Budget)
        budgetLineItems = budgetData["PROFIT & LOSS"]["REVENUE"]["LineItems"]["Revenue"]

        rows = []

        # ----------- BUILD ROWS ------------
        for itemName, values in actualLineItems.items():

            print(itemName,values,'----------3333333333333333333---------------')

            # Actual
            currentActual = get_total(values, year, currentMonths)
            previousActual = get_total(values, year, prevMonths)
            actualYTD = get_total(values, year, list(range(1, currentMonths[0] + 1)))

            # Budget
            budgetValues = budgetLineItems.get(itemName, [])
            budgetCurrent = get_total(budgetValues, year, currentMonths)
            budgetYTD = get_total(budgetValues, year, list(range(1, currentMonths[0] + 1)))

            # Variances
            varianceBudget = currentActual - budgetCurrent
            varianceLastMonth = currentActual - previousActual

            # ----------- REMOVE ROW IF SUM OF ALL NUMBERS == 0 ------------
            numeric_values = [
                currentActual, previousActual, budgetCurrent,
                varianceBudget, varianceLastMonth,
                actualYTD, budgetYTD
            ]

            # if sum(numeric_values) == 0:
            #     continue  # skip this row

            # ----------- APPEND ROW ------------
            rows.append([
                ValueObjectModel(Value=itemName, isPositive=True, Type="", Symbol=""),

                ValueObjectModel(Value=currentActual, isPositive=True, Type="currency", Symbol="$"),
                ValueObjectModel(Value=previousActual, isPositive=True, Type="currency", Symbol="$"),
                ValueObjectModel(Value=budgetCurrent, isPositive=True, Type="currency", Symbol="$"),
                ValueObjectModel(Value=varianceBudget, isPositive=True, Type="currency", Symbol="$"),
                ValueObjectModel(Value=varianceLastMonth, isPositive=True, Type="currency", Symbol="$"),
                ValueObjectModel(Value=actualYTD, isPositive=True, Type="currency", Symbol="$"),
                ValueObjectModel(Value=budgetYTD, isPositive=True, Type="currency", Symbol="$"),
            ])

        # ----------- ADD TOTAL ROW ------------
        if rows:
            numeric_total_count = len(rows[0]) - 1
            totals = [0] * numeric_total_count

            for r in rows:
                for i in range(1, len(r)):
                    totals[i-1] += r[i].Value if isinstance(r[i].Value, (int, float)) else 0

            total_row = [ValueObjectModel(Value="Total", isPositive=True, Type="", Symbol="")]

            for t in totals:
                total_row.append(
                    ValueObjectModel(Value=t, isPositive=True, Type="currency", Symbol="$")
                )

            rows.append(total_row)

        # ----------- BUILD TABLE MODEL ------------
        table = TableModel(
            Id="REVENUE_VARIANCE",
            Title="Revenue Variance Table",
            Column=columns,
            Rows=rows,
            TableType="Variance",
            Visibility=True,
            KpiType="Actuals"
        )

        return Result(Data=table, Status=1, Message="Done")

    except Exception as ex:
        message = f"Error in varianceTable: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
