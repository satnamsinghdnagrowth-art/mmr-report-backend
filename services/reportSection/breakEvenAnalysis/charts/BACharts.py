from datetime import datetime
from core.models.base.ResultModel import Result
from typing import Optional
from config.FunctionMaping import functionRegistry
from helper.GetValueSum import getValueSum
from helper.LoadJsonData import financialDataTest
from helper.GetFileByReportId import getReportData
from helper.GetValueSymbol import getValueSymbol
from services.calculations.Revenue import totalRevenue
from services.calculations.Expenses import totalOperatingExpenses
from services.calculations.BreakEvenMargin import breakEven
from core.models.visualsModel.ChartModel import (
    ChartDataModel,
    YAxisSeriesModel,
    MarkerModel,
)


def getBACharts(
    year: int,
    months: list[int],
    reportId: Optional[int] = None,
) -> Result:
    try:
        totalRev = totalRevenue(year, months, reportId).Data
        fixedCost = totalOperatingExpenses(year, months, reportId).Data
        breakEvenValue = breakEven(year, months, reportId).Data

        variableCost = 1 - (totalRev / fixedCost)

        revenue = list(range(0, 3200001, 200000))
        fixed_costs = [fixedCost] * len(revenue)
        total_costs = [fixedCost + (variableCost * r) for r in revenue]

        valueData = getValueSymbol("Revenue")

        valueType = valueData["type"]
        valueSymbol = valueData["symbol"]

        yAxisSeries = [
            YAxisSeriesModel(
                Title="Revenue",
                Values=revenue,
                Type="Line",
                UnitType=valueType,
                Symbol=valueSymbol,
            ),
            YAxisSeriesModel(
                Title="Total Costs",
                Values=total_costs,
                Type="Line",
                UnitType=valueType,
                Symbol=valueSymbol,
            ),
            YAxisSeriesModel(
                Title="Fixed Cost",
                Values=fixed_costs,
                Type="Line",
                UnitType=valueType,
                Symbol=valueSymbol,
            ),
        ]

        # Convert integers to strings for Xaxis
        xaxis_labels = [str(x) for x in revenue]

        # Markers Objects
        markerObjRevenue = MarkerModel(
            Label="Revenue",
            Xvalue=totalRev,
            Yvalue=totalRev,
            Color="green",
            Shape="bullseye",
            Size=8,
            Description=totalRev,
        )
        markerObjTotalCost = MarkerModel(
            Label="total Cost",
            Xvalue=totalRev,
            Yvalue=fixedCost,
            Color="red",
            Shape="bullseye",
            Size=8,
            Description=fixedCost,
        )
        markerObjBreakPoint = MarkerModel(
            Label="BreakEven Point",
            Xvalue=breakEvenValue,
            Yvalue=breakEvenValue,
            Color="black",
            Shape="bullseye",
            Size=8,
            Description=breakEvenValue,
        )

        chartData = ChartDataModel(
            Title="Cash Flow Chart",
            Xaxis=xaxis_labels,
            YaxisSeries=yAxisSeries,
            IndexAxis="x",
            RightYaxis=False,
            Markers=[markerObjRevenue, markerObjBreakPoint, markerObjTotalCost],
        )

        return Result(
            Data=[chartData], Status=1, Message="chart chart generated successfully"
        )

    except Exception as e:
        print(f"{datetime.now()} Error generating chart: {e}")
        return Result(Data=None, Status=0, Message="Chart generation failed.")
