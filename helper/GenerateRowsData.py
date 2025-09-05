from helper.GetValueSum import getValueSum
from core.models.visualsModel.ValueObject import ValueObjectModel
from helper.GetCurrentPrevPeriods import getCurrentAndPreviousPeriods
import calendar


def generateChangeRow(title, financialData, pathKeys, year, staticMonths, isAsset):
    row = [ValueObjectModel(Value=title, isPositive=True, Type="", Symbol="")]

    for m, y in staticMonths:
        currentYear, currentMonths, prevYear, prevMonths = getCurrentAndPreviousPeriods(
            y, [m], "month"
        )

        sumThis = getValueSum(financialData, pathKeys, currentYear, currentMonths).Data
        sumPrev = getValueSum(financialData, pathKeys, prevYear, prevMonths).Data

        result = sumThis - sumPrev

        if isAsset:
            result = -result  # reverse for asset

        row.append(
            ValueObjectModel(
                Value=result,
                isPositive=True,
                Type="currency",
                Symbol="$",
            )
        )

    return row


def generateChangeValueRow(title, financialData, pathKeys, year, staticMonths, isAsset):
    row = []

    for m, y in staticMonths:
        currentYear, currentMonths, prevYear, prevMonths = getCurrentAndPreviousPeriods(
            y, [m], "month"
        )

        sumThis = getValueSum(financialData, pathKeys, currentYear, currentMonths).Data
        sumPrev = getValueSum(financialData, pathKeys, prevYear, prevMonths).Data

        result = sumThis - sumPrev

        if isAsset:
            result = -result  # reverse for asset

        row.append(
            result
        )

    return row


def calculateSectionTotal(section_rows, staticMonths, title):
    totals = []
    for col_index in range(1, len(staticMonths) + 1):
        col_sum = 0
        for row in section_rows:
            if len(row) > col_index:
                val = row[col_index].Value
                if isinstance(val, (int, float)):
                    col_sum += val
        totals.append(col_sum)

    total_row = [
        ValueObjectModel(
            Value=f"Cash Flow from {title}", isPositive=True, Type="", Symbol=""
        )
    ] + [
        ValueObjectModel(Value=val, isPositive=(val >= 0), Type="currency", Symbol="$")
        for val in totals
    ]
    return total_row
