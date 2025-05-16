from datetime import datetime
from core.models.base.ResultModel import Result
from core.models.visualsModel.TableModel import TableModel
from helper.LoadJsonData import financialDataTest
from services.calculations.DiffrenceCalculation import diffrenceAndPercentage
from helper.metricCheck import isMetricPositive
from helper.GetFileByReportId import getReportData
import calendar
from helper.GetCurrentPrevPeriods import getCurrentAndPreviousPeriods
from core.models.visualsModel.ValueObject import ValueObjectModel


# Get the sections tables
def getRevenueTable(year: int, months, reportId, reportType):
    try:
        financialData = financialDataTest
        if reportId is not None:
            financialData = getReportData(reportId)

        title = "Revenue Channels Comparison"
        revenueData = financialData["PROFIT & LOSS"]["REVENUE"]["LineItems"]["Revenue"]

        currentYear, currentMonths, prevYear, prevMonths = getCurrentAndPreviousPeriods(
            year, months, reportType
        )

        if reportType.lower() == "year":
            Headers = [
                "Income Statement",
                f"{currentYear} Year",
                f"{prevYear} Year",
                "This Year vs Last Year($)",
                "This Year vs Last Year(%)",
            ]
        else:
            Headers = [
                "Income Statement",
                f"{calendar.month_abbr[currentMonths[0]]} Month",
                f"{calendar.month_abbr[prevMonths[0]]} Month",
                "This Month vs Last Month($)",
                "This Month vs Last Month(%)",
            ]
        rows = []

        totalCurrentData = 0
        totalPrevData = 0

        for key, data in revenueData.items():
            filteredDataCurrent = [
                entry
                for entry in data
                if entry["Year"] == currentYear and entry["Month"] in currentMonths
            ]
            totalSum = sum(item["Value"] for item in filteredDataCurrent)

            filteredDataPrev = [
                entry
                for entry in data
                if entry["Year"] == prevYear and entry["Month"] in prevMonths
            ]
            totalSumPrev = sum(item["Value"] for item in filteredDataPrev)

            if totalSum == 0.0 and totalSumPrev == 0.0:
                continue

            totalCurrentData += totalSum
            totalPrevData += totalSumPrev

            result = diffrenceAndPercentage(totalSum, totalSumPrev).Data

            rows.append(
                [
                    ValueObjectModel(Value=key, isPositive=True, Type="", Symbol=""),
                    ValueObjectModel(
                        Value=totalSum,
                        isPositive=isMetricPositive(title, totalSum),
                        Type="currency",
                        Symbol="$",
                    ),
                    ValueObjectModel(
                        Value=totalSumPrev,
                        isPositive=isMetricPositive(title, totalSumPrev),
                        Type="currency",
                        Symbol="$",
                    ),
                    ValueObjectModel(
                        Value=result["Diffrence"],
                        isPositive=isMetricPositive(title, result["Diffrence"]),
                        Type="currency",
                        Symbol="$",
                    ),
                    ValueObjectModel(
                        Value=result["PercentChange"],
                        isPositive=isMetricPositive(title, result["PercentChange"]),
                        Type="percentage",
                        Symbol="%",
                    ),
                ]
            )

        totalValueresult = diffrenceAndPercentage(totalCurrentData, totalPrevData).Data

        rows.append(
            [
                ValueObjectModel(
                    Value="Total Revenue", isPositive=True, Type="", Symbol=""
                ),
                ValueObjectModel(
                    Value=round(totalCurrentData, 2),
                    isPositive=isMetricPositive(title, totalCurrentData),
                    Type="currency",
                    Symbol="$",
                ),
                ValueObjectModel(
                    Value=round(totalPrevData, 2),
                    isPositive=isMetricPositive(title, totalPrevData),
                    Type="currency",
                    Symbol="$",
                ),
                ValueObjectModel(
                    Value=totalValueresult["Diffrence"],
                    isPositive=isMetricPositive(title, totalValueresult["Diffrence"]),
                    Type="currency",
                    Symbol="$",
                ),
                ValueObjectModel(
                    Value=totalValueresult["PercentChange"],
                    isPositive=isMetricPositive(
                        title, totalValueresult["PercentChange"]
                    ),
                    Type="percentage",
                    Symbol="%",
                ),
            ]
        )

        return Result(
            Data=TableModel(Title=title, Column=Headers, Rows=rows),
            Status=1,
            Message="Revenue Card calculated successfully",
        )

    except Exception as ex:
        message = f"Error occurred at getRevenueTable: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
