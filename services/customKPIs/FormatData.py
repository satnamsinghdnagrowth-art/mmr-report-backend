import pandas as pd
from core.models.base.ResultModel import Result
from config.FilesBaseDIR import CUSTOM_KPIS_DATA_UPLOAD_DIR
import json
import os


def _custom_kpi_data_path(reportId) -> str:
    """Canonical path for a report's processed custom KPI data JSON."""
    return os.path.join(CUSTOM_KPIS_DATA_UPLOAD_DIR, str(reportId), f"CustomFile_{reportId}.json")


# Data formatting of custom files
def dataFormatting(filePath, reportId: int) -> Result:
    try:
        # Read Excel file
        df = pd.read_excel(filePath, skiprows=4)

        # Normalise column names so minor whitespace / casing differences don't fail
        df.columns = [str(c).strip() for c in df.columns]

        expected_first_col = "Custom KPIs"
        if df.columns[0].lower() != expected_first_col.lower():
            return Result(
                Status=0,
                Message=(
                    f"File format is incorrect. "
                    f"Expected first column to be '{expected_first_col}' "
                    f"(row 5 after skipping 4 header rows), "
                    f"but found '{df.columns[0]}'."
                ),
            )

        result = {"Report Id": int(reportId), "Custom KPIs": {}}

        for _, row in df.iterrows():
            kpi_name = str(row[df.columns[0]]).strip()
            if not kpi_name or kpi_name.lower() == "nan":
                continue
            result["Custom KPIs"][kpi_name] = []

            for col in df.columns[1:]:
                if not isinstance(col, str) or "Unnamed" in col or " " not in col:
                    continue
                try:
                    month_str, year_str = col.split()
                    month_number = pd.to_datetime(month_str, format="%b").month
                except Exception:
                    continue

                value = row[col]
                if pd.notna(value):
                    result["Custom KPIs"][kpi_name].append(
                        {"Month": month_number, "Value": float(value), "Year": int(year_str)}
                    )

        # Write processed JSON to the canonical predictable location
        output_path = _custom_kpi_data_path(reportId)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        return Result(
            Data=result,
            Status=1,
            Message="Data formatted and saved successfully.",
        )

    except Exception as e:
        return Result(Status=0, Message=str(e))
