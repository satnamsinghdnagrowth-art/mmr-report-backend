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
    YaxisControllerModel,
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

        if totalRev == 0 or fixedCost == 0:
            raise ValueError("Total Revenue or Fixed Cost is zero. Cannot build chart.")

        # Calculate contribution margin
        cm_percent = fixedCost / breakEvenValue
        variable_cost_percent = 1 - cm_percent

        print()

        # Revenue range for X-axis
        revenue = list(range(0, int(breakEvenValue * 2) + 1, 1500))

        # Series calculations
        fixed_costs = [fixedCost] * len(revenue)

        # Calculate variable costs
        total_costs = [fixedCost + (variable_cost_percent * r) for r in revenue]

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
            Title="",
            Xaxis=xaxis_labels,
            YaxisSeries=yAxisSeries,
            IndexAxis="x",
            RightYaxis=False,
            YaxisController=[
                YaxisControllerModel(Id="left", Orientation="left", Unit="$")
            ],
            Markers=[markerObjBreakPoint],
        )

        return Result(
            Data=[chartData], Status=1, Message="chart chart generated successfully"
        )

    except Exception as e:
        print(f"{datetime.now()} Error generating chart: {e}")
        return Result(Data=None, Status=0, Message="Chart generation failed.")
