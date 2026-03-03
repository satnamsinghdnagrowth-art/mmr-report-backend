from datetime import datetime
from core.models.base.ResultModel import Result
import calendar
from typing import Optional
from helper.GetValueSymbol import getValueSymbol
from config.FunctionMaping import functionRegistry
from core.models.visualsModel.ChartModel import (
    ChartDataModel,
    YAxisSeriesModel,
    YaxisControllerModel,
)
from config.FilesBaseDIR import BUDGET_DATA_UPLOAD_DIR
from core.models.base.SourceModel import SourceDataTypes
from helper.GetFinancialData import checkFileExistance
from core.models.base.ColorModel import COLORS

def retrieveChart(
    year: int,
    months: list[int],
    config: dict,
    reportType: Optional[str] = None,
    reportId: Optional[int] = None,
) -> Result:
    try:

        title = config["title"]
        rigthYaxis = config["rigthYaxis"]
        chartData = config["data"]
        axisChoice = config["indexAxis"]
        visualId = config["visualId"]
        
        # Handle different report types
        if reportType and reportType.lower() == "month":
            current_month = months[0]  # assume latest month is passed
            last_six_months = []
            for i in range(5, -1, -1):
                month = current_month - i
                y = year
                if month <= 0:
                    month += 12
                    y -= 1
                last_six_months.append((y, month))
            months = last_six_months
            month_groups = [[m] for y, m in months]  # Each month is its own group

        elif reportType and reportType.lower() == "quarter":
            # Generate quarters for the year
            quarters = [
                (year, [1, 2, 3]),  # Q1
                (year, [4, 5, 6]),  # Q2
                (year, [7, 8, 9]),  # Q3
                (year, [10, 11, 12]),  # Q4
            ]
            months = quarters
            month_groups = [
                q[1] for q in quarters
            ]  # Extract month lists for processing

        else:
            months = [(year, m) for m in months]
            month_groups = [[m] for y, m in months]

        # Generate X-axis labels
        first_label = chartData[0]["label"].lower()
        current_year = datetime.now().year

        if reportType and reportType.lower() == "quarter":
            # Quarter labels
            if first_label == "current year" or str(current_year) in first_label:
                xAxis = [f"Q{i + 1}" for i in range(len(months))]
            else:
                xAxis = [f"Q{i + 1} {y}" for i, (y, _) in enumerate(months)]
        elif first_label == "current year" or str(current_year) in first_label:
            xAxis = [
                f"{calendar.month_abbr[m]}" for (y, m) in months if isinstance(m, int)
            ]
        else:
            xAxis = [
                f"{calendar.month_abbr[m]} {y}"
                for (y, m) in months
                if isinstance(m, int)
            ]

        yAxisSeries = []
        symbolList = []

        # Process each metric
        for index,metric in enumerate(chartData):

            # Get source type FIRST
            sourceType = metric.get("sourceType", None)


            # Normalize source type
            if sourceType == "Budget" or sourceType == SourceDataTypes.Budget:
                sourceType = SourceDataTypes.Budget
            else:
                sourceType = SourceDataTypes.Actuals

            # Budget file check must be done AFTER knowing sourceType
            if sourceType == SourceDataTypes.Budget:
                budget_file = f"{BUDGET_DATA_UPLOAD_DIR}/{reportId}/BudgetFile_{reportId}.json"

                if not checkFileExistance(budget_file):

                    print(f"Budget file missing → Skipping metric: {metric.get('label')}")
                    continue


            valueFunc = metric["valueFunc"]
            label = metric["label"]
            functionName = metric["funcName"]

            valueData = getValueSymbol(valueFunc)
            valueType = valueData["type"]
            valueSymbol = valueData["symbol"]
            symbolList.append(valueSymbol)

            yaxisId = metric["yaxisId"]

            func = functionRegistry.get(functionName)
            
            if not func:
                raise ValueError(f"Function '{functionName}' not found in registry.")

            values = []

            # Iterate through periods (months or quarters)
            for idx, (y, month_list) in enumerate(months):
                try:
                    actual_year = y - 1 if "Last Year" in label else y

                    # Get the appropriate month list
                    if reportType and reportType.lower() == "quarter":
                        month = month_list  # Already a list of months for the quarter
                    else:
                        month = (
                            month_list if isinstance(month_list, list) else [month_list]
                        )

                    result = func(actual_year, month, reportId,sourceType)

                    data = result.Data

                except Exception as error:
                    data = 0
                    period_name = (
                        f"Q{idx + 1}"
                        if reportType and reportType.lower() == "quarter"
                        else calendar.month_name[
                            month_list[0]
                            if isinstance(month_list, list)
                            else month_list
                        ]
                    )
                    print(
                        f"{datetime.now()} Error fetching '{label}' for {period_name} {y}: {error}"
                    )
                values.append(data)

            # Skip series with all zeros
            if all(v == 0.0 for v in values):
                print(f"Skipping '{label}' because all values are zero.")
                continue

            yAxisSeries.append(
                YAxisSeriesModel(
                    Title=label,
                    Values=values,
                    Type=metric["type"],
                    UnitType=valueType,
                    Symbol=valueSymbol,
                    AreaFill=metric["AreaFill"],
                    YaxisId=yaxisId,
                    Color=COLORS[index]
                )
            )

        # Deduplicate symbols and create axis controllers
        unique_symbols = set(symbolList)

        yaxisControllers = []

        if unique_symbols == {"%"} or unique_symbols == {"$"}:
            # All values have the same unit
            symbol = symbolList[0] if symbolList else "$"  # Default to "$" if empty
            yaxisControllers.append(
                YaxisControllerModel(Id="left", Orientation="left", Unit=symbol)
            )
        else:
            # Mixed symbols: % and $
            yaxisControllers.append(
                YaxisControllerModel(Id="right", Orientation="right", Unit="%")
            )
            yaxisControllers.append(
                YaxisControllerModel(Id="left", Orientation="left", Unit="$")
            )

        chartData = ChartDataModel(
            Title=title,
            Xaxis=xAxis,
            YaxisSeries=yAxisSeries,
            IndexAxis=axisChoice,
            RightYaxis=rigthYaxis,
            YaxisController=yaxisControllers,
            Id=visualId,
            KpiType="Actuals",
        )

        return Result(
            Data=chartData, Status=1, Message=f"{title} chart generated successfully"
        )

    except Exception as error:
        message = f"Error generating chart: {error}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
