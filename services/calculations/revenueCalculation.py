from datetime import datetime
from config.variable import variableMapping
from core.models.base.ResultModel import Result

def calculateRevenue(data,classification):
    # try:
    #     revenueCode = variableMapping["PROFIT & LOSS"]["REVENUE"]

    #     revenueDF = data[data["Classification"].isin(revenueCode)]

    #     month_cols = [
    #         col
    #         for col in revenueDF.columns
    #         if col not in ["Classification", "Account Name"]
    #     ]

    #     total_revenue = revenueDF[month_cols].fillna(0).sum().sum()


    #     # Create a dictionary with total revenue for each month
    #     monthly_totals = {
    #         month: revenueDF[month].fillna(0).sum() for month in month_cols
    #     }

    #     result_data = {"Revenue": monthly_totals}

    #     # Return the monthly totals
    #     return Result(
    #         Data=result_data,
    #         Status=1,
    #         Message="Month-wise revenue calculated successfully",
    #     )

        # print(revenueDF["Oct 2024"])

        # oct_2024_total = revenueDF["Jul 2024"].fillna(0).sum()

        # return Result(
        #     Data=oct_2024_total, Status=1, Message="Calculation done successfully"
        # )

    # except Exception as ex:
    #     message = f"Error occur at calculateRevenue: {ex}"
    #     print(f"{datetime.now()} {message}")
    #     return Result(Status=0, Message=message)

    result_dict = {}


    for section, subcategories in variableMapping.items():
        print(section, "this is section")
        result_dict[section] = {}  # Initialize the section key

        for subcategory, codes in subcategories.items():
            for code in codes:
                # Filter rows for current classification code
                code_df = data[data["Classification"] == code]

                # Extract month columns
                month_cols = [
                    col
                    for col in code_df.columns
                    if col not in ["Classification", "Account Name"]
                ]

                # Sum each month and store in a dictionary
                monthly_data = {
                    month: float(code_df[month].fillna(0).sum()) for month in month_cols
                }

                result_dict[section][code] = monthly_data  # Nest under section

    return Result(
        Data=result_dict,
        Status=1,
        Message="Monthly totals by classification code calculated successfully",
    )
