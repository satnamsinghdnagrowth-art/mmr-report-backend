from typing import Dict
import calendar
import traceback
from datetime import datetime

from core.models.base.ResultModel import Result
from core.models.visualsModel.ChartModel import (
    ChartDataModel,
    YaxisControllerModel,
    YAxisSeriesModel,
)
from helper.GetValueSymbol import getValueSymbol


def format_chart_data(filtered_data: Dict):
    """
    Format filtered KPI data into chart structure with multiple series
    """
    try:
        custom_kpis = filtered_data.get("Custom KPIs", {})
        # --- Get only the first key ---
        first_key = next(iter(custom_kpis.keys()), None)

        if not custom_kpis:
            raise ValueError("No Custom KPI data available for chart formatting.")

        # --- Collect all unique (month, year) pairs ---
        all_months = set()
        for kpi_values in custom_kpis.values():
            for entry in kpi_values:
                month = entry.get("Month")
                year = entry.get("Year")
                if month and year:
                    all_months.add((month, year))

        if not all_months:
            raise ValueError("No valid month/year data found in KPI entries.")

        # --- Sort months chronologically ---
        sorted_months = sorted(all_months, key=lambda x: (x[1], x[0]))

        # --- Build X-axis labels ---
        xaxis = [
            f"{calendar.month_abbr[month]} {year}"
            for month, year in sorted_months
        ]

        # --- Build Y-axis series (one per KPI) ---
        yaxis_series = []
        yaxis_controllers = {}
        axis_index = 0

        for kpi_name, kpi_values in custom_kpis.items():
            if not kpi_values:
                continue

            # Lookup values by (month, year)
            value_lookup = {
                (entry.get("Month"), entry.get("Year")): entry.get("Value", 0)
                for entry in kpi_values
            }

            values = [
                round(value_lookup.get((month, year), 0), 2)
                for month, year in sorted_months
            ]

            # Determine unit type and symbol
            unit_entities = getValueSymbol(kpi_name)
            yaxis_id = f"y{axis_index}"

            # Create Y-axis controller per unit type
            if yaxis_id not in yaxis_controllers:
                yaxis_controllers[yaxis_id] = YaxisControllerModel(
                    Id=yaxis_id,
                    Orientation="left" if axis_index == 0 else "right",
                    Unit=unit_entities.get("symbol"),
                )

            series = YAxisSeriesModel(
                Title=kpi_name,
                Type="Line",
                UnitType=unit_entities.get("type"),
                Symbol=unit_entities.get("symbol"),
                AreaFill=False,
                Values=values,
                YaxisId=yaxis_id,
            )

            yaxis_series.append(series)
            axis_index += 1

        # --- Build chart model ---
        chart = ChartDataModel(
            Id=f"custom_kpi_chart_{first_key}_{filtered_data.get('Report Id', '')}",
            Title=f"{first_key}",
            Xaxis=xaxis,
            YaxisSeries=yaxis_series,
            IndexAxis="x",
            RightYaxis=len(yaxis_controllers) > 1,
            YaxisController=list(yaxis_controllers.values()),
            KpiType="Custom",
        )

        return chart

    except Exception as ex:
        error_trace = traceback.format_exc()
        message = f"Error occurred in format_chart_data: {ex}"

        print(f"{datetime.now()} {message}")
        print(error_trace)

        return Result(
            Status=0,
            Message=message
        )
