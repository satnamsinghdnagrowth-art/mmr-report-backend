import pandas as pd
from core.models.base.ResultModel import Result
import json
from datetime import datetime


def dataFormatting(filePath) -> Result:
    try:
        # Read Excel file
        df = pd.read_excel(filePath, skiprows=4)

        df.rename(columns={df.columns[0]: "Custom KPIs"}, inplace=True)

        result = {"Report Id": 243455, "Custom KPIs": {}}

        for _, row in df.iterrows():
            kpi_name = row["Custom KPIs"]
            result["Custom KPIs"][kpi_name] = []

            for col in df.columns[1:]:
                # ✅ Skip invalid column names (e.g., NaN, Unnamed, empty)
                if not isinstance(col, str) or "Unnamed" in col or " " not in col:
                    continue

                try:
                    month_str, year_str = col.split()
                    month_number = pd.to_datetime(month_str, format="%b").month
                except Exception as e:
                    print(col,"***************************")
                    print(e)
                    print("------------------------------------------------------")
                    continue  # skip malformed columns safely

                value = row[col]

                if pd.notna(value):
                    result["Custom KPIs"][kpi_name].append(
                        {"Month": month_number, "Value": value, "Year": int(year_str)}
                    )

        with open("database/customKPIs/1234.json", "w") as f:
            data = json.dump(result, f, indent=2)

        return Result(Data=result, Status=1, Message="Data format successfully.")

    except Exception as ex:
        message = f"Error occurred in dataFormatting: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
