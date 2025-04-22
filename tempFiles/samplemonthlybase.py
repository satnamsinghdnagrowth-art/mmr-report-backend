from helper.readExcel import readExcelFile
from datetime import datetime
from collections import defaultdict
from config.variable import variableMapping
from core.models.base.ResultModel import Result
import pandas as pd
from dateutil.relativedelta import relativedelta


def retriveBSAccountNames(category: str, month: str):
    try:
        filePath = "tempFiles/Honest Game Corporation Jan 2025 (4).xlsx"
        excelData = readExcelFile(filePath)
        data = excelData.Data

        cleanedData = data[~data["Classification"].isnull()]
        result = defaultdict(dict)
        BSData = variableMapping[category]

        month_dt = pd.to_datetime(month, format="%b %Y")

        # Create a dictionary of month labels with previous, current, and next month
        month_list = {
            f"Last Month - {(month_dt - relativedelta(months=1)).strftime('%b %Y')}": (
                month_dt - relativedelta(months=1)
            ).strftime("%b %Y"),
            f"This Month - {month_dt.strftime('%b %Y')}": month_dt.strftime("%b %Y"),
            f"Next Month - {(month_dt + relativedelta(months=1)).strftime('%b %Y')}": (
                month_dt + relativedelta(months=1)
            ).strftime("%b %Y"),
        }

        for main, category in BSData.items():
            for code in category:
                classification = list(code.keys())[0]
                displayname = list(code.values())[0]

                # Filter the rows based on classification
                matches = cleanedData[cleanedData["Classification"] == classification]
                matches = matches.drop(columns=["Classification", "Account Name"])

                print(
                    f"Available columns: {matches.columns.tolist()}"
                )  # Debugging line

                # Filter columns based on the available months in the data
                filtered_cols = [
                    col for col in matches.columns if col in month_list.values()
                ]
                print(f"Filtered columns: {filtered_cols}")  # Debugging line

                # If there are missing months, handle the missing data by assigning 0
                monthly_totals = {
                    label: matches[col].fillna(0).sum()
                    for label, col in zip(month_list.keys(), filtered_cols)
                }

                result[main][displayname] = monthly_totals

        return Result(Data=result, Status=1, Message="Success")

    except Exception as ex:
        message = f"Error occurred at retriveBSAccountNames: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
