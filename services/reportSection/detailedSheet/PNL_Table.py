from datetime import datetime
from core.models.base.ResultModel import Result
from helper.LoadJsonData import financialDataTest
from helper.GetFileByReportId import getReportData
from core.models.visualsModel.TableModel import TableModel
from services.calculations.GrossProfit import grossProfit, grossProfitMargin
from services.calculations.Ebit import EBIT
from helper.GenerateCalculatedRows import generateSummaryRow
from services.calculations.EarningBefore import (
    earningBeforeTax,
)
from helper.GetValueSum import getValueSum
from services.calculations.Ebit import EBIT
from services.calculations.GrossProfit import operatingProfit
from services.calculations.NetIncome import netIncome, netIncomeMargin
from core.models.visualsModel.ValueObject import ValueObjectModel
import calendar


def getProfitLossTable(year: int, months, tableTypes: list[str], reportId):
    try:
        financialData = (
            getReportData(reportId)["Financial Data"] if reportId else financialDataTest
        )

        reportDatarange = getReportData(reportId)["Report Details"]["Data Range"]

        available_months = sorted(
            [(d["Month"], d["Year"]) for d in reportDatarange],
            key=lambda x: (x[1], x[0]),  # Sort by year, then month
        )

        available_months_set = set(available_months)

        combinedRows = []
        combinedHeaders = None

        tableType = tableTypes[0]

        data = financialData[tableType]
        last_month = max(months)

        # Get last 6 months (month, year) pairs
        staticMonths = []
        current_month = last_month
        current_year = year

        for _ in range(6):
            if (current_month, current_year) in available_months_set:
                staticMonths.insert(0, (current_month, current_year))
            current_month -= 1
            if current_month == 0:
                current_month = 12
                current_year -= 1

        # Correct headers
        if tableType == "PROFIT & LOSS":
            headers = (
                [tableType]
                + [f"{calendar.month_abbr[m]} {y}" for (m, y) in staticMonths]
                + ["Total"]
            )
        else:
            headers = [tableType] + [
                f"{calendar.month_abbr[m]} {y}" for (m, y) in staticMonths
            ]

        if combinedHeaders is None:
            combinedHeaders = headers

        rows = []

        for sectionName, sectionContent in data.items():
            sectionRows = []

            sectionRows.insert(
                1,
                [
                    ValueObjectModel(
                        Value=sectionName, isPositive=True, Type="", Symbol=""
                    )
                ],
            )

            sectionMonthlyTotals = {(m, y): 0.0 for (m, y) in staticMonths}

            for subSectionName, subSectionContent in sectionContent[
                "LineItems"
            ].items():
                monthlyTotals = {(m, y): 0.0 for (m, y) in staticMonths}

                subSectionRows = []

                for itemLabel, itemData in subSectionContent.items():
                    rowData = [
                        ValueObjectModel(
                            Value=itemLabel, isPositive=True, Type="", Symbol=""
                        )
                    ]
                    monthlySum = 0.0

                    for m, y in staticMonths:
                        val = next(
                            (
                                item["Value"]
                                for item in itemData
                                if item["Month"] == m and item["Year"] == y
                            ),
                            0.0,
                        )
                        monthlySum += val
                        monthlyTotals[(m, y)] += val
                        sectionMonthlyTotals[(m, y)] += val

                        rowData.append(
                            ValueObjectModel(
                                Value=val,
                                isPositive=True,
                                Type="currency",
                                Symbol="$",
                            )
                        )

                    if monthlySum == 0.0:
                        continue

                    rowData.append(
                        ValueObjectModel(
                            Value=monthlySum,
                            isPositive=True,
                            Type="currency",
                            Symbol="$",
                        )
                    )
                    subSectionRows.append(rowData)

                sectionRows.extend(subSectionRows)

            sectionGrandTotal = sum(sectionMonthlyTotals.values())

            totalSectionRow = [
                ValueObjectModel(
                    Value=f"Total {sectionName}",
                    isPositive=True,
                    Type="",
                    Symbol="",
                )
            ]

            for m, y in staticMonths:
                totalSectionRow.append(
                    ValueObjectModel(
                        Value=sectionMonthlyTotals[(m, y)],
                        isPositive=True,
                        Type="currency",
                        Symbol="$",
                    )
                )

            totalSectionRow.append(
                ValueObjectModel(
                    Value=sectionGrandTotal,
                    isPositive=True,
                    Type="currency",
                    Symbol="$",
                )
            )

            sectionRows.append(totalSectionRow)

            if sectionName.upper() == "EXPENSES":
                rows.append(
                    generateSummaryRow(
                        "Gross Profit",
                        year,
                        staticMonths,
                        lambda y, m: grossProfit(y, m, reportId).Data,
                    )
                )
                rows.append(
                    generateSummaryRow(
                        "Gross Profit Margin(%)",
                        year,
                        staticMonths,
                        lambda y, m: grossProfitMargin(y, m, reportId).Data,
                    )
                )

            if sectionName.upper() == "OTHER INCOME":
                rows.append(
                    generateSummaryRow(
                        "Operating Profit",
                        year,
                        staticMonths,
                        lambda y, m: operatingProfit(y, m, reportId).Data,
                    )
                )

            if sectionName.upper() == "INTEREST INCOME":
                rows.append(
                    generateSummaryRow(
                        "Earning Before Interest & Tax",
                        year,
                        staticMonths,
                        lambda y, m: EBIT(y, m, reportId).Data,
                    )
                )

            if sectionName.upper() == "DIVIDEND":
                rows.append(
                    generateSummaryRow(
                        "Earnings Before Tax",
                        year,
                        staticMonths,
                        lambda y, m: earningBeforeTax(y, m, reportId).Data,
                    )
                )
                rows.append(
                    generateSummaryRow(
                        "Net Income",
                        year,
                        staticMonths,
                        lambda y, m: netIncome(y, m, reportId).Data,
                    )
                )
                rows.append(
                    generateSummaryRow(
                        "Net Income Margin(%)",
                        year,
                        staticMonths,
                        lambda y, m: netIncomeMargin(y, m, reportId).Data,
                    )
                )

            if sectionGrandTotal == 0.0:
                continue

            rows.extend(sectionRows)

        combinedRows.extend(rows)

        if tableTypes[0] == "PROFIT & LOSS":
            tableTypes[0] = "Detailed Financial Statements (Last 6 months)"
        else:
            tableTypes[0] = ""

        tableObj = TableModel(
            Title=tableTypes[0], Column=combinedHeaders, Rows=combinedRows
        )
        return Result(
            Data=tableObj, Status=1, Message="Combined tables generated successfully"
        )

    except ZeroDivisionError as ex:
        print(f"{datetime.now()} ZeroDivisionError: {ex}")
        return Result(Data=None, Status=0, Message=f"ZeroDivisionError: {ex}")

    except Exception as ex:
        print(f"{datetime.now()} Exception: {ex}")
        return Result(Data=None, Status=0, Message=f"Exception: {ex}")
