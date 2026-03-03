# services/customKPIs/visualCreation/CustomCardCreation.py

from typing import Dict, Any
import calendar
import hashlib
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
from helper.GenerateVisualId import generate_visual_id


def _derive_card_id(base_id: str, kpi_name: str) -> str:
    """Derive a stable, deterministic child ID from the parent VisualId + KPI name."""
    name_hash = hashlib.md5(kpi_name.encode()).hexdigest()[:8]
    return f"{base_id}_{name_hash}"


def format_card_data(filtered_data: Dict[str, Any], payload=None):
    """
    Format Custom KPI data into a list of CardDataModels,
    one for each selected KPI.
    """
    try:
        custom_kpis = filtered_data.get("Custom KPIs", {})

        if not custom_kpis:
            raise ValueError("No Custom KPI data available for card formatting.")

        cards_list = []

        # Generate a fallback base ID if payload visual ID is missing to ensure uniqueness per card later
        base_visual_id = None
        if hasattr(payload, 'VisualId') and payload.VisualId:
            base_visual_id = payload.VisualId

        for kpi_name, kpi_values in custom_kpis.items():
            if not kpi_values:
                continue

            # --- Collect all unique (month, year) pairs for this KPI ---
            all_months = set()
            for entry in kpi_values:
                month = entry.get("Month")
                year = entry.get("Year")
                if month and year:
                    all_months.add((month, year))

            if not all_months:
                continue

            # --- Sort months chronologically ---
            sorted_months = sorted(all_months, key=lambda x: (x[1], x[0]))

            # --- Aggregate KPI values per month (SUM) for this specific KPI ---
            aggregated_values = []
            for month, year in sorted_months:
                month_total = sum(
                    entry.get("Value", 0)
                    for entry in kpi_values
                    if entry.get("Month") == month and entry.get("Year") == year
                )
                aggregated_values.append(round(month_total, 2))

            # --- Latest & previous values ---
            main_value = aggregated_values[-1] if aggregated_values else 0
            prev_value = aggregated_values[-2] if len(aggregated_values) > 1 else 0

            # --- Value type / symbol ---
            unit_entities = getValueSymbol(kpi_name)

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

            # --- Use stored ID or generate fallback per card ---
            # For multiple cards from one payload: derive stable ID from base_visual_id + kpi_name_hash
            # This ensures the ID is the same on every reload, so frontend metadata lookups succeed.
            if base_visual_id:
                visual_id = _derive_card_id(base_visual_id, kpi_name)
            else:
                # Fallback for legacy KPIs without a stored VisualId. Generates a fully stable deterministic ID.
                fallback_base = f"custom_legacy_card_{hashlib.md5(kpi_name.encode('utf-8')).hexdigest()[:8]}"
                visual_id = _derive_card_id(fallback_base, kpi_name)

            # --- Single aggregated card ---
            card = CardDataModel(
                Id=visual_id,
                Title=kpi_name,
                Content=main_value_obj,
                Footer=footer,
                KpiType="Custom",
            )
            cards_list.append(card)

        return cards_list

    except Exception as ex:
        error_trace = traceback.format_exc()
        message = f"Error occurred in format_card_data: {ex}"
        print(f"{datetime.now()} {message}")
        print(error_trace)
        return Result(
            Status=0,
            Message=message
        )
