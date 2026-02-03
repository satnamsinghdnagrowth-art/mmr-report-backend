from typing import Dict, Any
import calendar
import traceback
from datetime import datetime

from core.models.base.ResultModel import Result
from core.models.visualsModel.ValueObject import ValueObjectModel
from core.models.visualsModel.TableModel import TableModel
from helper.GetValueSymbol import getValueSymbol
from helper.GenerateVisualId import generate_visual_id


def format_table_data(filtered_data: Dict[str, Any], payload=None):
    """
    Format filtered KPI data into a table structure.
    """
    try:
        custom_kpis = filtered_data.get("Custom KPIs", {})
        # --- Get only the first key ---
        first_key = next(iter(custom_kpis.keys()), None)
        if not custom_kpis:
            raise ValueError("No Custom KPI data available for table formatting.")

        # --- Collect all unique (month, year) pairs ---
        all_months = set()
        for kpi_values in custom_kpis.values():
            for entry in kpi_values or []:
                month = entry.get("Month")
                year = entry.get("Year")
                if month is not None and year is not None:
                    all_months.add((month, year))

        if not all_months:
            raise ValueError("No valid month/year data found in KPI entries.")

        # --- Sort months chronologically (Year, Month) ---
        sorted_months = sorted(all_months, key=lambda x: (x[1], x[0]))

        # --- Build table columns ---
        columns = ["KPI Name"]
        columns.extend(
            f"{calendar.month_abbr[month]} {year}"
            for month, year in sorted_months
        )

        rows = []

        # --- Build table rows ---
        for kpi_name, kpi_values in custom_kpis.items():
            if not kpi_values:
                continue

            unit_entities = getValueSymbol(kpi_name)

            # KPI name column
            row = [
                ValueObjectModel(
                    Value=kpi_name,
                    isPositive=True,
                    Type="",
                    Symbol=""
                )
            ]

            # Lookup values by (month, year)
            value_lookup = {
                (entry.get("Month"), entry.get("Year")): entry.get("Value")
                for entry in kpi_values
            }

            # Fill month-wise values
            for month, year in sorted_months:
                value = value_lookup.get((month, year))

                row.append(
                    ValueObjectModel(
                        Value=round(value, 2) if value is not None else "-",
                        isPositive=True,
                        Type=unit_entities.get("type"),
                        Symbol=unit_entities.get("symbol"),
                    )
                )

            rows.append(row)

        # --- Generate unique ID ---
        payload_params = payload.__dict__ if payload and hasattr(payload, '__dict__') else None
        visual_id = generate_visual_id('table', filtered_data, payload_params)

        return TableModel(
            Id=visual_id,
            Title=f"{first_key}",
            Column=columns,
            Rows=rows,
            TableType="Tabular",
            Visibility=True,
            KpiType="Custom",
        )

    except Exception as ex:
        error_trace = traceback.format_exc()
        message = f"Error occurred in format_table_data: {ex}"

        print(f"{datetime.now()} {message}")
        print(error_trace)

        return Result(
            Status=0,
            Message=message
        )
