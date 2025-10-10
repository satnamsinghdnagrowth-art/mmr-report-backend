from core.models.visualsModel.ValueObject import ValueObjectModel
from core.models.visualsModel.TableModel import TableModel
from typing import Dict
import calendar
from datetime import datetime
from core.models.base.ResultModel import Result
from helper.GetValueSymbol import getValueSymbol


def format_table_data(filtered_data: Dict) -> Dict:
    try:
        """
        Format filtered KPI data into table structure
        """

        # Collect all unique months across all KPIs
        all_months = set()
        for kpi_values in filtered_data["Custom KPIs"].values():
            for entry in kpi_values:
                all_months.add((entry["Month"], entry["Year"]))

        # Sort months by year and month
        sorted_months = sorted(list(all_months), key=lambda x: (x[1], x[0]))

        # Build columns: KPI Name + Month columns
        columns = ["KPI Name"]
        for month, year in sorted_months:
            month_name = calendar.month_abbr[month]
            columns.append(f"{month_name} {year}")

        # Build rows - one row per KPI
        rows = []
        for kpi_name, kpi_values in filtered_data["Custom KPIs"].items():
            if not kpi_values:  # Skip empty KPIs
                continue

            row = [
                ValueObjectModel(Value=kpi_name, isPositive=True, Type="", Symbol="")
            ]

            # Create a lookup dictionary for quick access
            value_lookup = {
                (entry["Month"], entry["Year"]): entry["Value"] for entry in kpi_values
            }

            # Fill in values for each month (use "-" or 0 for missing values)
            for month, year in sorted_months:
                value = value_lookup.get((month, year))
                unitEntities = getValueSymbol(kpi_name)
                if value is not None:
                    value = value_lookup.get((month, year), 0)
                    response = ValueObjectModel(
                        Value=round(value, 2),
                        isPositive=True,
                        Type=unitEntities["type"],
                        Symbol=unitEntities["symbol"],
                    )

                    row.append(response)

                else:
                    row.append("-")  # or use 0 if you prefer

            rows.append(row)

        table = TableModel(
            Title="Custom KPI Table",
            Column=columns,
            Rows=rows,
            TableType= "Tabular",
            Visibility=True,
        )

        return {"Tables": [table]}
    except Exception as ex:
        message = f"Error occurred in format_chart_data: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)

