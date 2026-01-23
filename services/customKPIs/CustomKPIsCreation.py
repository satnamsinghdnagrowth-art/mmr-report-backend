from core.models.base.ResultModel import Result
import json
import os
import traceback
from datetime import datetime
from services.customKPIs.visualCreation.CustomChartCreation import format_chart_data
from services.customKPIs.visualCreation.CustomTableCreation import format_table_data
from services.customKPIs.visualCreation.CustomCardCreation import format_card_data

REPORT_JSON_PATH = "database/ReportTable.json"


def customKPICreation(payload, reportId) -> Result:
    try:
        visualtype = str(payload.VisualType).lower()
        year = int(payload.Year)
        month = int(payload.Months[0])  # First selected month
        items = payload.Items or []

        custom_file_path = None

        # --- Find Custom KPI file path for the report ---
        if os.path.exists(REPORT_JSON_PATH):
            with open(REPORT_JSON_PATH, "r", encoding="utf-8") as f:
                reports = json.load(f)

            for report in reports:
                if report.get("ReportId") == int(reportId):
                    custom_file_path = report.get("CustomKPIFilePath")
                    break

        if not custom_file_path or not os.path.exists(custom_file_path):
            raise FileNotFoundError("Custom KPI file not found for this report.")

        # --- Load KPI data ---
        with open(custom_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # --- Calculate last 6 months (year, month) pairs ---
        last_six_months = []
        y, m = year, month
        for _ in range(6):
            last_six_months.append((y, m))
            m -= 1
            if m == 0:
                m = 12
                y -= 1

        # --- Filter data ---
        filtered_data = {
            "Report Id": data.get("Report Id"),
            "Custom KPIs": {}
        }

        # If items not provided, include all KPIs
        if not items:
            items = list(data.get("Custom KPIs", {}).keys())

        for item in items:
            if item not in data.get("Custom KPIs", {}):
                continue

            kpi_entries = data["Custom KPIs"][item]
            filtered_entries = []

            for entry in kpi_entries:
                entry_year = entry.get("Year")
                entry_month = entry.get("Month")

                if (entry_year, entry_month) in last_six_months:
                    filtered_entries.append(entry)

            if filtered_entries:
                filtered_data["Custom KPIs"][item] = filtered_entries

        # --- Format output based on visual type ---
        if visualtype == "table":
            table_data = format_table_data(filtered_data)
            return Result(
                Data=table_data,
                Status=1,
                Message=f"Data filtered for last 6 months up to {month}-{year} (table format)."
            )

        elif visualtype == "chart":
            chart_data = format_chart_data(filtered_data)
            return Result(
                Data=chart_data,
                Status=1,
                Message=f"Data filtered for last 6 months up to {month}-{year} (chart format)."
            )
        elif visualtype == "card":
            card_data = format_card_data(filtered_data)
            return Result(
                Data=card_data,
                Status=1,
                Message=f"Data filtered for last 6 months up to {month}-{year} (card format)."
            )
        
        return Result(
            Data=filtered_data,
            Status=1,
            Message=f"Data filtered for last 6 months up to {month}-{year} successfully."
        )

    except Exception as ex:
        error_trace = traceback.format_exc()
        message = f"Error occurred in customKPICreation: {ex}"

        print(f"{datetime.now()} {message}")
        print(error_trace)

        return Result(
            Status=0,
            Message=message
        )
