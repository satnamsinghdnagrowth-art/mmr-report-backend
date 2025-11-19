from core.models.visualsModel.ValueObject import ValueObjectModel
from typing import Dict
import calendar
from datetime import datetime
from core.models.base.ResultModel import Result
from core.models.visualsModel.ChartModel import (
    ChartDataModel,
    YaxisControllerModel,
    YAxisSeriesModel,
)
from helper.GetValueSymbol import getValueSymbol


def format_chart_data(filtered_data: Dict) -> Dict:
    try:
        """
        Format filtered KPI data into chart structure with multiple series
        """

        # Collect all unique months across all KPIs
        all_months = set()
        for kpi_values in filtered_data["Custom KPIs"].values():
            for entry in kpi_values:
                all_months.add((entry["Month"], entry["Year"]))

        # Sort months by year and month
        sorted_months = sorted(list(all_months), key=lambda x: (x[1], x[0]))

        # Build X-axis labels
        xaxis = []
        for month, year in sorted_months:
            month_name = calendar.month_abbr[month]
            xaxis.append(f"{month_name} {year}")

        # Build Y-axis series - one series per KPI
        yaxis_series = []

        for kpi_name, kpi_values in filtered_data["Custom KPIs"].items():
            if not kpi_values:  # Skip empty KPIs
                continue

            # Create a lookup dictionary for quick access
            value_lookup = {
                (entry["Month"], entry["Year"]): entry["Value"] for entry in kpi_values
            }

            # Fill in values for each month
            values = []
            for month, year in sorted_months:
                value = value_lookup.get((month, year), 0)

                values.append(round(value, 2))

            # Determine unit type and symbol based on KPI name
            unitEntities = getValueSymbol(kpi_name)

            series = YAxisSeriesModel(
                Title=kpi_name,
                Type="Line",
                UnitType=unitEntities["type"],
                Symbol=unitEntities["symbol"],
                AreaFill=False,
                Values=values,
                YaxisId="left",
            )

            yaxis_series.append(series)

        # Build Y-axis controller
        yaxis_controller = YaxisControllerModel(
            Id="left", Orientation="left", Unit=unitEntities["symbol"]
        )

        chart = ChartDataModel(
            Title="Custom KPI Data",
            Xaxis=xaxis,
            YaxisSeries=yaxis_series,
            IndexAxis="y",
            RightYaxis=False,
            YaxisController=[yaxis_controller],
            KpiType="Custom",
        )

        return chart

    except Exception as ex:
        message = f"Error occurred in format_chart_data: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
