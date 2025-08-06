import pandas as pd
import json

# Load the Excel sheet
df = pd.read_excel("tempFiles/Budget comparison .xlsx",sheet_name='test')

# 2️⃣ Initialize the result dict
result = {}
current_section = None

# 3️⃣ Loop through the rows
for index, row in df.iterrows():
    kpi = str(row['KPI']).strip()

    # If the row is a section header, create a new section
    if kpi in [
        "Core Saas Metrics",
        "Sales & Growth",
        "Go-to-Market",
        "Capital Efficiency",
        "Profitability"
    ]:
        current_section = kpi
        result[current_section] = []
        continue

    # Skip empty or invalid rows
    if pd.isna(kpi) or kpi == 'nan' or current_section is None:
        continue

    # 4️⃣ Create a KPI dict
    kpi_data = {
        "KPI": kpi,
        "This Month": row['This Month'],
        "Last Month": row['Last Month'],
        "Variance": row['Variance'],
        "Variance %": row['Variance %'],
        "YTD": row['YTD'],
    }

    # 5️⃣ Add to the current section
    result[current_section].append(kpi_data)

# 6️⃣ Save to a JSON file
with open("kpi_report.json", "w") as f:
    json.dump(result, f, indent=2)

print("✅ JSON file created: kpi_report.json")
