import pandas as pd
from core.models.base.ResultModel import Result
import json
import os

REPORT_JSON_PATH = "database/ReportTable.json"

# Data formatting of custom files
def dataFormatting(filePath, reportId: int) -> Result:
    try:
        # Read Excel file
        df = pd.read_excel(filePath, skiprows=4)

        expected_first_col = "Custom KPIs"
        if df.columns[0] != expected_first_col:
            return Result(Status=0, Message="File format is not correct..")

        result = {"Report Id": reportId, "Custom KPIs": {}}

        for _, row in df.iterrows():
            kpi_name = row["Custom KPIs"]
            result["Custom KPIs"][kpi_name] = []

            for col in df.columns[1:]:
                # Skip invalid column names (e.g., NaN, Unnamed, empty)
                if not isinstance(col, str) or "Unnamed" in col or " " not in col:
                    continue

                try:
                    month_str, year_str = col.split()
                    month_number = pd.to_datetime(month_str, format="%b").month
                except Exception:
                    continue  # skip malformed columns safely

                value = row[col]

                if pd.notna(value):
                    result["Custom KPIs"][kpi_name].append(
                        {"Month": month_number, "Value": value, "Year": int(year_str)}
                    )

        output_dir = f"database/customKPIs/{reportId}"
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, f"CustomFile_{reportId}.json")
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)

        # Now update main report list file
        report_list_path = REPORT_JSON_PATH # your master JSON list

        if os.path.exists(report_list_path):
            with open(report_list_path, "r") as f:
                reports = json.load(f)

            updated = False
            for item in reports:
                if item["ReportId"] == int(reportId):
                    item["CustomKPIFilePath"] = output_path.replace("\\", "/")
                    updated = True
                    break

            if not updated:
                raise ValueError(f"ReportId {reportId} not found in reports.json")

            with open(report_list_path, "w") as f:
                json.dump(reports, f, indent=4)
        else:
            raise FileNotFoundError("reports.json file not found in 'database/' folder")

        return Result(Data=result, Status=1, Message="Data formatted successfully and report list updated.")

    except Exception as e:
        return Result(Status=0, Message=str(e))
