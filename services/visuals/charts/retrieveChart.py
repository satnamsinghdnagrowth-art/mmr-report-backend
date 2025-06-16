from datetime import datetime
from core.models.base.ResultModel import Result
import calendar
from typing import Optional
from helper.GetValueSymbol import getValueSymbol
from config.FunctionMaping import functionRegistry
from core.models.visualsModel.ChartModel import ChartDataModel, YAxisSeriesModel


from typing import Optional
from datetime import datetime
import calendar

def retrieveChart(
    year: int,
    months: list[int],
    title: str,
    chartData: list[dict],
    rigthYaxis: str,
    axisChoice: str,
    reportType: Optional[str] = None,
    reportId: Optional[int] = None,
) -> Result:
    try:
        if reportType and reportType.lower() == "month":
            current_month = months[0]  # assume latest month is passed
            last_six_months = []
            for i in range(4, -1, -1):
                month = current_month - i
                y = year
                if month <= 0:
                    month += 12
                    y -= 1
                last_six_months.append((y, month))
            months = last_six_months
        else:
            months = [(year, m) for m in months]

        first_label = chartData[0]["label"].lower()
        current_year = datetime.now().year
        if first_label == "current year" or str(current_year) in first_label:
            xAxis = [f"{calendar.month_abbr[m]}" for (y, m) in months]
        else:
            xAxis = [f"{calendar.month_abbr[m]} {y}" for (y, m) in months]


       
        yAxisSeries = []

        for metric in chartData:

            valueFunc = metric["valueFunc"]
            
            label = metric["label"]
            functionName = metric["funcName"]

            valueData = getValueSymbol(valueFunc)
            valueType = valueData["type"]
            valueSymbol = valueData["symbol"]

            func = functionRegistry.get(functionName) 


            if not func:
                raise ValueError(f"Function '{functionName}' not found in registry.")

            values = []
            for (y, m) in months:
                try:
                    actual_year = y - 1 if "Last Year" in label else y
                    result = func(actual_year, [m], reportId)
                    data = result.Data
                except Exception as error:
                    data = 0
                    print(f"{datetime.now()} Error fetchiwng '{label}' for {calendar.month_name[m]} {y}: {error}")
                values.append(data)

            yAxisSeries.append(
                YAxisSeriesModel(
                    Title=label,
                    Values=values,
                    Type=metric["type"],
                    UnitType=valueType,
                    Symbol=valueSymbol,
                    AreaFill=metric["AreaFill"],
                )
            )

        chartData = ChartDataModel(
            Title=title,
            Xaxis=xAxis,
            YaxisSeries=yAxisSeries,
            IndexAxis=axisChoice,
            RightYaxis=rigthYaxis,
        )


        return Result(
            Data=chartData,
            Status=1,
            Message=f"{title} chart generated successfully"
        )

    except Exception as error:
        message = f"Error generating chart: {error}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)

