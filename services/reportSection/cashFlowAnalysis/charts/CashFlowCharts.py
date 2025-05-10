from datetime import datetime
from core.models.base.ResultModel import Result
from typing import Optional
from config.FunctionMaping import functionRegistry
from helper.GetValueSum import getValueSum
from helper.LoadJsonData import financialDataTest
from helper.GetFileByReportId import getReportData
from services.calculations.Revenue import  totalRevenue
from services.calculations.Expenses import totalOperatingExpenses
from core.models.visualsModel.ChartModel import ChartDataModel, YAxisSeriesModel


def getCashFlowCharts(
    year: int,
    months: list[int],
    reportId: Optional[int] = None,
) -> Result:
    try:
        totalRev = totalRevenue(year, months, reportId).Data
        fixedCost = totalOperatingExpenses(year, months, reportId).Data

        variableCost = 1 - (totalRev / fixedCost)

        revenue = list(range(0, 3200001, 200000))
        fixed_costs = [fixedCost] * len(revenue)
        total_costs = [fixedCost + (variableCost * r) for r in revenue]

        yAxisSeries = [
            YAxisSeriesModel(Title="Revenue", Values=revenue, Type="Line"),
            YAxisSeriesModel(Title="Total Costs", Values=total_costs, Type="Line"),
            YAxisSeriesModel(Title="Fixed Cost", Values=fixed_costs, Type="Line"),
        ]

        # Convert integers to strings for Xaxis
        xaxis_labels = [str(x) for x in revenue]

        chartData = ChartDataModel(
            Title="Cash Flow Chart",
            Xaxis=xaxis_labels,
            YaxisSeries=yAxisSeries,
            IndexAxis="x"
        )

        return Result(
            Data=[chartData], Status=1, Message="chart chart generated successfully"
        )

    except Exception as e:
        print(f"{datetime.now()} Error generating chart: {e}")
        return Result(Data=None, Status=0, Message="Chart generation failed.")
