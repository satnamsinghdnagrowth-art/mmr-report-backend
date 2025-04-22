from helper.readExcel import readExcelFile
from datetime import datetime
from collections import defaultdict
from config.variable import variableMapping
from core.models.base.ResultModel import Result


# Analyze the data
def retriveBSAccountValues(category: str):
    try:
        filePath = "tempFiles/Honest Game Corporation Jan 2025 (4).xlsx"

        excelData = readExcelFile(filePath)

        data = excelData.Data

        cleanedData = data[~data["Classification"].isnull()]

        result = defaultdict(dict)

        BSData = variableMapping[category]

        for main, category in BSData.items():
            
            for code in category:

                classification = list(code.keys())[0]
                displayname = list(code.values())[0]

                matches = cleanedData[cleanedData["Classification"] == classification]

                matches = matches.drop(columns=["Classification", "Account Name"])

                month_cols = [col for col in matches.columns]

                monthly_totals = []
                for month in month_cols:
                    value = matches[month].fillna(0).sum()
                    try:
                        # Parse month-year string like 'Jan 2022' to datetime object
                        date_obj = datetime.strptime(month, "%b %Y")
                        monthly_totals.append(
                            {
                                "Month": date_obj.month,
                                "Year": date_obj.year,
                                "Value": round(value, 2),
                            }
                        )
                    except:
                        continue  # Skip malformed date columns

                result[main][displayname] = monthly_totals

        return Result(Data=result, Status=1, Message="Success")

    except Exception as ex:
        message = f"Error occur at retriveBSAccountNames: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
