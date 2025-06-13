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

        xAxis = [f"{calendar.month_abbr[m]}" for (y, m) in months]
        yAxisSeries = []

        for metric in chartData:
            label = metric["label"]
            functionName = metric["funcName"]

            valueData = getValueSymbol(label)
            valueType = valueData["type"]
            valueSymbol = valueData["symbol"]

            func = functionRegistry.get(functionName)
            if not func:
                raise ValueError(f"Function '{functionName}' not found in registry.")

            values = []
            for (y, m) in months:
                try:
                    actual_year = y - 1 if "Prev Year" in label else y
                    result = func(actual_year, [m], reportId)
                    data = result.Data
                except Exception as error:
                    data = 0
                    print(f"{datetime.now()} Error fetching '{label}' for {calendar.month_name[m]} {y}: {error}")
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


# def retrieveChart(
#     year: int,
#     months: list[int],
#     title: str,
#     chartData: list[dict],
#     rigthYaxis: str,
#     axisChoice: str,
#     reportType: Optional[str] = None,
#     reportId: Optional[int] = None,
# ) -> Result:
#     try:
#         print(reportType)

#         if reportType.lower() == "month":
#             months = range(1,months[0]+1)
        
#         xAxis = [f"{calendar.month_abbr[m]} " for m in months]

#         # xAxis = [f"{calendar.month_abbr[m]} {year}" for m in staticMonths]
#         yAxisSeries = []

#         for metric in chartData:
#             label = metric["label"]
#             functionName = metric["funcName"]

#             valueData = getValueSymbol(label)

#             valueType = valueData["type"]
#             valueSymbol = valueData["symbol"]

#             # Get the function from the registry
#             func = functionRegistry.get(functionName)
#             if not func:
#                 raise ValueError(f"Function '{functionName}' not found in registry.")

#             values = []

#             localYear = year - 1 if "Prev Year" in label else year

#             for month in months:
#                 try:
#                     result = func(localYear, [month], reportId)
#                     data = result.Data
#                 except Exception as error:
#                     data = 0  # fallback if error
#                     print(
#                         f"{datetime.now()} Error fetching '{label}' for month {month}: {error}"
#                     )
#                 values.append(data)

#             yAxisSeries.append(
#                 YAxisSeriesModel(
#                     Title=label,
#                     Values=values,
#                     Type=metric["type"],
#                     UnitType=valueType,
#                     Symbol=valueSymbol,
#                     AreaFill=metric["AreaFill"],
#                 )
#             )

#         chartData = ChartDataModel(
#             Title=title,
#             Xaxis=xAxis,
#             YaxisSeries=yAxisSeries,
#             IndexAxis=axisChoice,
#             RightYaxis=rigthYaxis,
#         )

#         return Result(
#             Data=chartData, Status=1, Message=f"{title} chart generated successfully"
#         )

#     except Exception as error:
#         message = f"Error generating chart: {error}"
#         print(f"{datetime.now()} {message}")
#         return Result(Status=0, Message=message)
