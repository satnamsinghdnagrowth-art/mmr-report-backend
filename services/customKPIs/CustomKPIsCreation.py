from core.models.base.ResultModel import Result
import json
import os
from datetime import datetime
from services.customKPIs.visualCreation.CustomChartCreation import format_chart_data
from services.customKPIs.visualCreation.CustomTableCreation import format_table_data

REPORT_JSON_PATH = "database/ReportTable.json"

def customKPICreation(payload, reportId) -> Result:
    try:
        visualtype = str(payload.VisualType).lower()
        startmonth = payload.StartMonth  # Expected: integer (1-12)
        endmonth = payload.EndMonth  # Expected: integer (1-12)
        items = payload.Items  # Expected: list of KPI names

        customFilePath = None

        report_list_path = REPORT_JSON_PATH # your master JSON list

        if os.path.exists(report_list_path):
            with open(report_list_path, "r") as f:
                reports = json.load(f)
                
            for item in reports:
                if item["ReportId"] == int(reportId):
                    customFilePath = item["CustomKPIFilePath"] 
                    break

        with open(customFilePath) as f:
            data = json.load(f)

        # Filter the data based on items and month range
        filtered_data = {"Report Id": data["Report Id"], "Custom KPIs": {}}

        # If items is empty or None, include all KPIs
        if not items:
            items = list(data["Custom KPIs"].keys())

        # Filter by selected items
        for item in items:
            if item in data["Custom KPIs"]:
                kpi_values = data["Custom KPIs"][item]

                # Filter by month range
                filtered_values = []
                for entry in kpi_values:
                    month = entry["Month"]

                    # Handle month range across year boundary
                    if startmonth <= endmonth:
                        # Normal range (e.g., March to June)
                        if startmonth <= month <= endmonth:
                            filtered_values.append(entry)
                    else:
                        # Range wraps around year (e.g., November to February)
                        if month >= startmonth or month <= endmonth:
                            filtered_values.append(entry)

                filtered_data["Custom KPIs"][item] = filtered_values

        # If visual type is table, format data accordingly
        if visualtype == "table":
            table_data = format_table_data(filtered_data)
            return Result(
                Data=table_data, Status=1, Message="Table data formatted successfully."
            )
        elif visualtype == "chart":
            chart_data = format_chart_data(filtered_data)
            return Result(
                Data=chart_data, Status=1, Message="Chart data formatted successfully."
            )
        else:
            # Return raw filtered data for other visual types
            return Result(
                Data=filtered_data, Status=1, Message="Data filtered successfully."
            )

    except Exception as ex:
        message = f"Error occurred in customKPICreation: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
