from datetime import datetime
from core.models.base.ResultModel import Result
from core.models.visualsModel.TableModel import TableModel
from helper.LoadJsonData import financialDataTest
from services.calculations.DiffrenceCalculation import diffrenceAndPercentage
from helper.metricCheck import isMetricPositive
from helper.GetFileByReportId import getReportData
from core.models.visualsModel.ValueObject import ValueObjectModel


# Get the sections cards
def getRevenueTable(year: int, months,reportId):
    try:
        financialData = financialDataTest

        if reportId is not  None:
             financialData = getReportData(reportId)

        title = "Revenue Channels Comparison"

        revenueData = financialData["PROFIT & LOSS"]["REVENUE"]["LineItems"]

        Headers = ["REVENUE", "2024", "2023", "This Year VS Prev Year($)", "Variance"]
        rows = []

        totalCurrentData = 0
        totalPrevData = 0

        for key, data in revenueData.items():
            filteredDataCurrent = [
                entry
                for entry in data
                if entry["Year"] == year and entry["Month"] in months
            ]
            totalSum = sum(item["Value"] for item in filteredDataCurrent)

            filteredDataPrev = [
                entry
                for entry in data
                if entry["Year"] == year - 1 and entry["Month"] in months
            ]
            totalSumPrev = sum(item["Value"] for item in filteredDataPrev)

            result = diffrenceAndPercentage(totalSum, totalSumPrev).Data

            # Skip the row if both current and previous sums are zero
            if totalSum == 0.0 and totalSumPrev == 0.0:
                continue

            totalCurrentData += totalSum
            totalPrevData += totalSumPrev

            # Create rows in the required format with ValueObjectModel instances
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

        # Calculate total values and append them to the rows
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

        # Create and return the table object
        tableObj = TableModel(
            Title="Revenue Channels Comparison", Column=Headers, Rows=rows
        )

        return Result(
            Data=tableObj, Status=1, Message="Revenue Card calculated successfully"
        )

    except Exception as ex:
        message = f"Error occurred at getRevenueTable: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
