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
from helper.LoadJsonData import financialDataTest
from helper.GetFileByReportId import getReportData
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import calendar
from dateutil.parser import parse


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

        financialData = getReportData(reportId)["Report Details"] if reportId else financialDataTest

        startDataRange = financialData.get("Data Range")[0]


        # Convert {'Month': 1, 'Year': 2025} into datetime
        if isinstance(startDataRange, dict) and "Month" in startDataRange and "Year" in startDataRange:
            startDate = datetime(startDataRange["Year"], startDataRange["Month"], 1)
        elif isinstance(startDataRange, str):
            startDate = parse(startDataRange)
        else:
            startDate = startDataRange  # fallback if already datetime


        # Main Content Cards Function
        mainFunc = functionRegistry.get(functionName)

        # Current Value
        mainValue = mainFunc(year, months, reportId).Data

        # Previous Value
        previousValue = 0

        if comparedTo.lower() in ["from last month", "from lastmonth"]:
            latest_month = months[0]
            prev_year, prev_month = (
                (year - 1, 12) if latest_month == 1 else (year, latest_month - 1)
            )
            previousValue = mainFunc(prev_year, [prev_month], reportId).Data

        elif comparedTo.lower() in ["from last year", "from lastyear"]:
            previousValue = mainFunc(year - 1, months, reportId).Data
        else:
            previousValue = None

        latest_month = max(months)
        latest_date = datetime(year, latest_month, 1)

        trend_dates = []

        for i in reversed(range(12)):
            month_date = latest_date - relativedelta(months=i)
            if month_date >= startDate:
                trend_dates.append(month_date)

        trendLineXaxis = [d.strftime("%b %Y") for d in trend_dates]
        trendLineYaxis = [mainFunc(d.year, [d.month], reportId).Data for d in trend_dates]

        trendLineData = TrendLineChart(Xaxis=trendLineXaxis, Yaxis=trendLineYaxis)

        mainValuePositiveCheck = isMetricPositive(title, mainValue)

        # Main Content Value Object
        contentValueObj = ValueObjectModel(
            Value=mainValue,
            isPositive=mainValuePositiveCheck,
            Type=valueType,
            Symbol=valueSymbol,
        )

        # Comparison value calculation
        prevValuePositiveCheck = isMetricPositive(title, previousValue)

        if comparisonFunc.lower() == "growthrate":
            comparisonValue = dataGrowthRate(mainValue, previousValue).Data
        else:
            comparisonValue = previousValue

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

        cardData = CardDataModel(
            Title=title,
            Content=contentValueObj,
            Footer=footerObj
        )

        return Result(
            Data=cardData,
            Status=1,
            Message="Card calculated successfully"
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at retrieveCard: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occurred at retrieveCard: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
