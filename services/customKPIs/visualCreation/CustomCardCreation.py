# services/customKPIs/visualCreation/CustomCardCreation.py

from typing import Dict, Any
import calendar
import traceback
from datetime import datetime

from core.models.base.ResultModel import Result
from core.models.visualsModel.CardModel import (
    TrendLineChart,
    CardDataModel,
    ValueObjectModel,
    FooterModel,
)
from helper.metricCheck import isMetricPositive
from helper.GetValueSymbol import getValueSymbol


def format_card_data(filtered_data: Dict[str, Any]):
    """
    Format Custom KPI data into a SINGLE CardDataModel
    with aggregated KPI values.
    """
    try:
        custom_kpis = filtered_data.get("Custom KPIs", {})

        # --- Get only the first key ---
        first_key = next(iter(custom_kpis.keys()), None)

        if not custom_kpis:
            raise ValueError("No Custom KPI data available for card formatting.")

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

        # --- Aggregate KPI values per month (SUM) ---
        aggregated_values = []
        for month, year in sorted_months:
            month_total = sum(
                entry.get("Value", 0)
                for kpi_values in custom_kpis.values()
                for entry in kpi_values
                if entry.get("Month") == month and entry.get("Year") == year
            )
            aggregated_values.append(round(month_total, 2))

        # --- Latest & previous values ---
        main_value = aggregated_values[-1]
        prev_value = aggregated_values[-2] if len(aggregated_values) > 1 else 0

        # --- Pick first KPI for value type / symbol ---
        first_kpi_name = next(iter(custom_kpis.keys()))
        unit_entities = getValueSymbol(first_kpi_name)

        value_type = unit_entities.get("type") or ""
        if value_type not in ("currency", "percentage", "months", ""):
            value_type = ""
        value_symbol = unit_entities.get("symbol") or ""

        # --- Trend line ---
        trend_line = TrendLineChart(
            Xaxis=[f"{calendar.month_abbr[month]} {year}" for month, year in sorted_months],
            Yaxis=aggregated_values,
        )

        # --- Main value ---
        main_value_obj = ValueObjectModel(
            Value=main_value,
            isPositive=isMetricPositive("Custom KPIs", main_value),
            Type=value_type,
            Symbol=value_symbol,
        )

        # --- Comparison value ---
        comparison_value = round(main_value - prev_value, 2)
        comparison_value_obj = ValueObjectModel(
            Value=comparison_value,
            isPositive=isMetricPositive("Custom KPIs", comparison_value),
            Type=value_type,
            Symbol=value_symbol,
        )

        # --- Footer ---
        footer = FooterModel(
            ComparisonValue=comparison_value_obj,
            ComparisonText="From last month",
            TrendLine=trend_line,
        )

        # --- Single aggregated card ---
        card = CardDataModel(
            Id=f"custom_kpi_card_{first_key}_{filtered_data.get('Report Id', '')}",
            Title=f"{first_key}",
            Content=main_value_obj,
            Footer=footer,
        )

        return card

    except Exception as ex:
        error_trace = traceback.format_exc()
        message = f"Error occurred in format_card_data: {ex}"
        print(f"{datetime.now()} {message}")
        print(error_trace)
        return Result(
            Status=0,
            Message=message
        )
