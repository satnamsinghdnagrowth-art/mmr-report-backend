from datetime import datetime
from core.models.visualsModel.CardModel import (
    TrendLineChart,
    CardDataModel,
    ValueObjectModel,
    FooterModel,
)
from core.models.base.ResultModel import Result
from typing import Any
import calendar
from config.MetricBehaviour import NEGATIVE_METRICS, PERCENTAGE_METRICS
from config.FunctionMaping import functionRegistry
from datetime import datetime
from helper.GetValueSymbol import getValueSymbol
from helper.metricCheck import isMetricPositive


def retrieveCard(
    year: int,
    months: list[int],
    title: str,
    functionName: str,
    comparisonFunc: str,
    comparedTo: str,
):
    try:
        valueData = getValueSymbol(title)

        valueType = valueData["type"]
        valueSymbol = valueData["symbol"]

        mainFunc = functionRegistry.get(functionName)

        trendFunc = functionRegistry.get(comparisonFunc)

        if comparedTo.lower() in ["from prev month", "from lastmonth"]:
            prev_year, prev_month = (
                (year - 1, 12) if months[0] == 1 else (year, months[0] - 1)
            )
            previous = trendFunc(prev_year, [0]).Data

        elif comparedTo.lower() in ["from prev year", "from lastyear"]:
            previous = trendFunc(year - 1, months).Data

        else:
            previous = None  # or handle as needed

        trendLineXaxis = [calendar.month_abbr[m] for m in range(1, 13)]

        trendLineYaxis = [mainFunc(year, [m]).Data for m in range(1, 13)]

        trendLineData = TrendLineChart(Xaxis=trendLineXaxis, Yaxis=trendLineYaxis)

        mainValue = mainFunc(year, months).Data

        mainValuePositiveCheck = isMetricPositive(title, mainValue)

        contentValueObj = ValueObjectModel(
            Value=mainValue,
            isPositive=mainValuePositiveCheck,
            Type=valueType,
            Symbol=valueSymbol,
        )

        prevValuePositiveCheck = isMetricPositive(title, previous)

        compValueObj = ValueObjectModel(
            Value=previous,
            isPositive=prevValuePositiveCheck,
            Type=valueType,
            Symbol=valueSymbol,
        )

        footerObj = FooterModel(
            ComparisonValue=compValueObj,
            ComparisonText=comparedTo,
            TrendLine=trendLineData,
        )

        cardData = CardDataModel(Title=title, Content=contentValueObj, Footer=footerObj)

        return Result(
            Data=cardData, Status=1, Message="Revenue Card calculated successfully"
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at retrieveCard: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occurred at retrieveCard: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
