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
from services.calculations.GrowthRate import dataGrowthRate


def retrieveCard(
    reportId: int,
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

        # Main Content Cards Funtion
        mainFunc = functionRegistry.get(functionName)

        # Current Value
        mainValue = mainFunc(year, months).Data

        previousValue = 0

        # previousValue value
        if comparedTo.lower() in ["from prev month", "from lastmonth"]:
            prev_year, prev_month = (
                (year - 1, 12) if months[0] == 1 else (year, months[0] - 1)
            )

            previousValue = mainFunc(prev_year, [prev_month], reportId).Data

        elif comparedTo.lower() in ["from prev year", "from lastyear"]:
            previousValue = mainFunc(year - 1, months, reportId).Data

        else:
            previousValue = None  #  handle as needed

        # TrendLine Data
        trendLineXaxis = [calendar.month_abbr[m] for m in range(1, 13)]

        trendLineYaxis = [mainFunc(year, [m], reportId).Data for m in range(1, 13)]

        trendLineData = TrendLineChart(Xaxis=trendLineXaxis, Yaxis=trendLineYaxis)

        mainValuePositiveCheck = isMetricPositive(title, mainValue)

        # Main Content Value Object
        contentValueObj = ValueObjectModel(
            Value=mainValue,
            isPositive=mainValuePositiveCheck,
            Type=valueType,
            Symbol=valueSymbol,
        )

        prevValuePositiveCheck = isMetricPositive(title, previousValue)

        if comparisonFunc.lower() == "growthrate":
            comparisonValue = dataGrowthRate(mainValue, previousValue).Data
        else:
            comparisonValue = previousValue

        # Footer Content Value Object
        compValueObj = ValueObjectModel(
            Value=comparisonValue,
            isPositive=prevValuePositiveCheck,
            Type="percentage",
            Symbol="%",
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
