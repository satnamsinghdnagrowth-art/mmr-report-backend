from datetime import datetime
from core.models.base.ResultModel import Result
from helper.LoadJsonData import SECTION_CARD_CONFIGS
from core.models.visualsModel.ChartModel import ChartDataModel, YAxisSeriesModel
from helper.LoadJsonData import financialDataTest
from helper.GetFileByReportId import getReportData
from helper.GetValueSymbol import getValueSymbol
from services.calculations.DiffrenceCalculation import diffrenceAndPercentage
from config.FunctionMaping import functionRegistry
from datetime import datetime
from typing import List


# Get the sections cards
def getRevenueBreakdownChart(year: int, months: list[int], reportId: int):
    try:
        financialData = financialDataTest

        if reportId is not None:
            financialData = getReportData(reportId)["Financial Data"]

        revenueData = financialData["PROFIT & LOSS"]["REVENUE"]["LineItems"]["Revenue"]

        xAxis = []

        yAxis = []

        for key, data in revenueData.items():
            filteredDataCurrent = [
                entry
                for entry in data
                if entry["Year"] == year and entry["Month"] in months
            ]

            totalSum = sum(item["Value"] for item in filteredDataCurrent)

            if totalSum == 0.0:
                continue

            yAxis.append(totalSum)
            xAxis.append(key)

        valueData = getValueSymbol("Revenue")

        valueType = valueData["type"]
        valueSymbol = valueData["symbol"]

        yAxisObj = YAxisSeriesModel(
            Title="Revenue",
            Type="bar",
            Values=yAxis,
            UnitType=valueType,
            Symbol=valueSymbol,
        )

        chartObj = ChartDataModel(
            Title="Revenue BreakDown",
            Xaxis=xAxis,
            YaxisSeries=[yAxisObj],
            IndexAxis="y",
            RightYaxis=False,
        )

        return Result(
            Data=chartObj, Status=1, Message="Revenue chart calculated successfully"
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at getRevenueBreakdownChart: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occurred at getRevenueBreakdownChart: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
