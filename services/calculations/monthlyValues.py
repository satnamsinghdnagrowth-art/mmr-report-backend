from datetime import datetime
from config.variable import variableMapping
from core.models.base.ResultModel import Result


def calculateMonthlyValues(data):
    try:
        resultDict = {}

        for section, subcategories in variableMapping.items():

            resultDict[section] = {} 

            for subcategory, codes in subcategories.items():
                for code in codes:
                    code_df = data[data["Classification"] == code]

                    month_cols = [
                        col
                        for col in code_df.columns
                        if col not in ["Classification", "Account Name"]
                    ]

                    # Sum each month and store in a dictionary
                    monthly_data = {
                        month: float(code_df[month].fillna(0).sum()) for month in month_cols
                    }

                    resultDict[section][code] = monthly_data  # Nest under section

        return Result(
            Data=resultDict,
            Status=1,
            Message="Monthly totals by classification code calculated successfully",
        )


    except Exception as ex:
        message = f"Error occur at calculateRevenue: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)

    