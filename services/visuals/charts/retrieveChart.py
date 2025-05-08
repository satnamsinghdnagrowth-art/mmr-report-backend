from datetime import datetime
from core.models.base.ResultModel import Result
import calendar
from typing import Optional
from config.FunctionMaping import functionRegistry
from core.models.visualsModel.ChartModel import ChartDataModel, YAxisSeriesModel


def retrieveChart(
    year: int, months: list[int], title: str, chartData: list[dict], axisChoice: str,reportType : Optional[str]=None,reportId : Optional[int]=None
) -> Result:
    try:
        staticMonths  = [1,2,3,4,5,6,7,8,9,10,11,12]
        xAxis = [f"{calendar.month_abbr[m]} {year}" for m in staticMonths]
        yAxisSeries = []

        for metric in chartData:
            label = metric["label"]
            functionName = metric["funcName"]

            # Get the function from the registry
            func = functionRegistry.get(functionName)
            if not func:
                raise ValueError(f"Function '{functionName}' not found in registry.")

            values = []

            localYear = year - 1 if "Prev Year" in label else year

            for month in months:
                try:
                    result = func(localYear, [month],reportId)
                    data = result.Data
                except Exception as error:
                    data = 0  # fallback if error
                    print(
                        f"{datetime.now()} Error fetching '{label}' for month {month}: {error}"
                    )
                values.append(data)

            yAxisSeries.append(
                YAxisSeriesModel(Title=label, Values=values, Type=metric["type"])
            )

        chartData = ChartDataModel(
            Title=title, Xaxis=xAxis, YaxisSeries=yAxisSeries, IndexAxis=axisChoice
        )

        return Result(
            Data=chartData, Status=1, Message=f"{title} chart generated successfully"
        )

    except Exception as error:
        message = f"Error generating chart: {error}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
