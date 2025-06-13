from datetime import datetime
from core.models.base.ResultModel import Result
from helper.LoadJsonData import financialDataTest
from helper.GetFileByReportId import getReportData
from core.models.visualsModel.TableModel import TableModel
from services.calculations.GrossProfit import grossProfit
from services.calculations.Expenses import totalOperatingExpenses
from services.calculations.Ebit import EBIT
from helper.GenerateCalculatedRows import generateSummaryRow
from services.calculations.EarningBefore import (
    earningBeforeTax,
)
from helper.GetValueSum import getValueSum
from services.calculations.NetIncome import netIncome
from core.models.visualsModel.ValueObject import ValueObjectModel
import calendar


def getDetailedTable(year: int, tableTypes: list[str], reportId):
    try:
        financialData = getReportData(reportId)["Financial Data"] if reportId else financialDataTest

        combinedRows = []
        combinedHeaders = None  # Set only once based on first table

        for tableIndex, tableType in enumerate(tableTypes):
            data = financialData[tableType]
            staticMonths = range(1, 6)

            # Setup headers
            if tableType == "PROFIT & LOSS":
                headers = [tableType] + [f"{calendar.month_abbr[m]} {year}" for m in staticMonths] + ["Total"]
            else:
                headers = [tableType] + [f"{calendar.month_abbr[m]} {year}" for m in staticMonths]

            if combinedHeaders is None:
                combinedHeaders = headers

            rows = []

            for sectionName, sectionContent in data.items():
                sectionRows = []
                sectionMonthlyTotals = {m: 0.0 for m in staticMonths}

                for subSectionName, subSectionContent in sectionContent["LineItems"].items():
                    monthlyTotals = {m: 0.0 for m in staticMonths}
                    subSectionRows = []

                    if tableType.lower() in ["balancesheet", "equity"]:
                        subSectionRows.append([
                            ValueObjectModel(Value=subSectionName, isPositive=True, Type="", Symbol="")
                        ])

                    for itemLabel, itemData in subSectionContent.items():
                        rowData = [
                            ValueObjectModel(Value=itemLabel, isPositive=True, Type="", Symbol="")
                        ]
                        filteredYearData = [item for item in itemData if item["Year"] == year]
                        monthlySum = 0.0

                        for month in staticMonths:
                            val = next((item["Value"] for item in filteredYearData if item["Month"] == month), 0.0)
                            monthlySum += val
                            monthlyTotals[month] += val
                            sectionMonthlyTotals[month] += val

                            rowData.append(
                                ValueObjectModel(Value=val, isPositive=True, Type="currency", Symbol="$")
                            )

                        if monthlySum == 0.0:
                            continue

                        if tableType == "PROFIT & LOSS":
                            rowData.append(ValueObjectModel(Value=monthlySum, isPositive=True, Type="currency", Symbol="$"))
                        subSectionRows.append(rowData)

                    if tableType.lower() in ["balancesheet", "equity"]:
                        grandTotal = sum(monthlyTotals.values())
                        if grandTotal != 0.0:
                            totalRow = [
                                ValueObjectModel(Value=f"Total {subSectionName}", isPositive=True, Type="", Symbol="")
                            ]
                            for month in staticMonths:
                                totalRow.append(
                                    ValueObjectModel(Value=monthlyTotals[month], isPositive=True, Type="currency", Symbol="$")
                                )
                            subSectionRows.append(totalRow)
                            sectionRows.extend(subSectionRows)
                    else:
                        sectionRows.extend(subSectionRows)

                sectionGrandTotal = sum(sectionMonthlyTotals.values())
                if sectionGrandTotal == 0.0:
                    continue

                sectionRows[0:0] = [[ValueObjectModel(Value=sectionName, isPositive=True, Type="", Symbol="")]]

                totalSectionRow = [ValueObjectModel(Value=f"Total {sectionName}", isPositive=True, Type="", Symbol="")]
                for month in staticMonths:
                    totalSectionRow.append(
                        ValueObjectModel(Value=sectionMonthlyTotals[month], isPositive=True, Type="currency", Symbol="$")
                    )

                if tableType == "PROFIT & LOSS":
                    totalSectionRow.append(
                        ValueObjectModel(Value=sectionGrandTotal, isPositive=True, Type="currency", Symbol="$")
                    )
                    sectionRows.append(totalSectionRow)

                if sectionName.upper() == "COST OF SALES":
                    sectionRows.append(generateSummaryRow("Gross Profit", year, staticMonths, lambda y, m: grossProfit(y, [m], reportId).Data))

                if sectionName.upper() == "OTHER INCOME":
                    sectionRows.append(generateSummaryRow("Earnings Before Interest & Tax", year, staticMonths, lambda y, m: EBIT(y, [m], reportId).Data))

                    sectionRows.append([ValueObjectModel(Value="Interest Income", isPositive=True, Type="currency", Symbol="$")])

                    interestIncome = [ValueObjectModel(Value="Interest Earned", isPositive=True, Type="currency", Symbol="$")]
                    for month in staticMonths:
                        result = getValueSum(financialData, ["PROFIT & LOSS", "OTHER INCOME", "Classification", "Interest Income"], year, [month]).Data
                        interestIncome.append(ValueObjectModel(Value=result, isPositive=True, Type="currency", Symbol="$"))
                    sectionRows.append(interestIncome)

                    sectionRows.append(generateSummaryRow("Earnings Before Tax", year, staticMonths, lambda y, m: earningBeforeTax(y, [m], reportId).Data))
                    sectionRows.append(generateSummaryRow("Total Net Income", year, staticMonths, lambda y, m: netIncome(y, [m], reportId).Data))

                rows.extend(sectionRows)

            # Prepend a row to mark the table title
            # combinedRows.append([ValueObjectModel(Value=f"{tableType} Statement", isPositive=True, Type="", Symbol="")])
            combinedRows.extend(rows)

        tableObj = TableModel(Title=tableTypes[0], Column=combinedHeaders, Rows=combinedRows)

        return Result(Data=tableObj, Status=1, Message="Combined tables generated successfully")

    except ZeroDivisionError as ex:
        message = f"ZeroDivisionError in getDetailedTable: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)

    except Exception as ex:
        message = f"Exception in getDetailedTable: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
