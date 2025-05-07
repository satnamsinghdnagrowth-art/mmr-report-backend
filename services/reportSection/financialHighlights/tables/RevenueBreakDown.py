from datetime import datetime
from core.models.base.ResultModel import Result
from core.models.visualsModel.TableModel import TableModel
from helper.LoadJsonData import financialDataTest
from services.calculations.DiffrenceCalculation import diffrenceAndPercentage
from helper.metricCheck import isMetricPositive
from core.models.visualsModel.ValueObject import ValueObjectModel


# Get the sections cards
def getRevenueTable(year: int, months):
    try:
        title = "Revenue Channels Comparison"
        revenueData = financialDataTest["PROFIT & LOSS"]["REVENUE"]["LineItems"]

        Headers = ["REVENUE", "2024", "2023", "This Year VS Prev Year($)", "Variance"]
        rows = []

        totalCurrentData = 0
        totalPrevData = 0

        for key, data in revenueData.items():
            filteredDataCurrent = [
                entry
                for entry in data
                if entry["Year"] == year and entry["Month"] in months
            ]
            totalSum = sum(item["Value"] for item in filteredDataCurrent)

            filteredDataPrev = [
                entry
                for entry in data
                if entry["Year"] == year - 1 and entry["Month"] in months
            ]
            totalSumPrev = sum(item["Value"] for item in filteredDataPrev)

            result = diffrenceAndPercentage(totalSum, totalSumPrev).Data

            # Skip the row if both current and previous sums are zero
            if totalSum == 0.0 and totalSumPrev == 0.0:
                continue

            totalCurrentData += totalSum
            totalPrevData += totalSumPrev

            # Create rows in the required format with ValueObjectModel instances
            rows.append(
                [
                    ValueObjectModel(Value=key, isPositive=True, Type="", Symbol=""),
                    ValueObjectModel(
                        Value=totalSum,
                        isPositive=isMetricPositive(title, totalSum),
                        Type="currency",
                        Symbol="$",
                    ),
                    ValueObjectModel(
                        Value=totalSumPrev,
                        isPositive=isMetricPositive(title, totalSumPrev),
                        Type="currency",
                        Symbol="$",
                    ),
                    ValueObjectModel(
                        Value=result["Diffrence"],
                        isPositive=isMetricPositive(title, result["Diffrence"]),
                        Type="currency",
                        Symbol="$",
                    ),
                    ValueObjectModel(
                        Value=result["PercentChange"],
                        isPositive=isMetricPositive(title, result["PercentChange"]),
                        Type="percentage",
                        Symbol="%",
                    ),
                ]
            )

        # Calculate total values and append them to the rows
        totalValueresult = diffrenceAndPercentage(totalCurrentData, totalPrevData).Data

        rows.append(
            [
                ValueObjectModel(
                    Value="Total Revenue", isPositive=True, Type="", Symbol=""
                ),
                ValueObjectModel(
                    Value=round(totalCurrentData, 2),
                    isPositive=isMetricPositive(title, totalCurrentData),
                    Type="currency",
                    Symbol="$",
                ),
                ValueObjectModel(
                    Value=round(totalPrevData, 2),
                    isPositive=isMetricPositive(title, totalPrevData),
                    Type="currency",
                    Symbol="$",
                ),
                ValueObjectModel(
                    Value=totalValueresult["Diffrence"],
                    isPositive=isMetricPositive(title, totalValueresult["Diffrence"]),
                    Type="currency",
                    Symbol="$",
                ),
                ValueObjectModel(
                    Value=totalValueresult["PercentChange"],
                    isPositive=isMetricPositive(
                        title, totalValueresult["PercentChange"]
                    ),
                    Type="percentage",
                    Symbol="%",
                ),
            ]
        )

        # Create and return the table object
        tableObj = TableModel(
            Title="Revenue Channels Comparison", Column=Headers, Rows=rows
        )

        return Result(
            Data=tableObj, Status=1, Message="Revenue Card calculated successfully"
        )

    except Exception as ex:
        message = f"Error occurred at getRevenueTable: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)


# from datetime import datetime
# from core.models.base.ResultModel import Result
# from helper.LoadJsonData import SECTION_CARD_CONFIGS
# from core.models.visualsModel.TableModel import TableModel
# from helper.LoadJsonData import financialDataTest
# from services.calculations.DiffrenceCalculation import diffrenceAndPercentage
# from config.FunctionMaping import functionRegistry
# from datetime import datetime


# # Get the sections cards
# def getRevenueTable(year: int, months):
#     try:
#         revenueData = financialDataTest["PROFIT & LOSS"]["REVENUE"]["LineItems"]

#         Headers = ["REVENUE", "2024", "2023", "This Year VS Prev Year($)", "Variance"]

#         values = []

#         totalCurrentData = 0
#         totalPrevData = 0

#         for key, data in revenueData.items():
#             filteredDataCurrent = [
#                 entry
#                 for entry in data
#                 if entry["Year"] == year and entry["Month"] in months
#             ]

#             totalSum = sum(item["Value"] for item in filteredDataCurrent)

#             filteredDataPrev = [
#                 entry
#                 for entry in data
#                 if entry["Year"] == year - 1 and entry["Month"] in months
#             ]

#             totalSumPrev = sum(item["Value"] for item in filteredDataPrev)

#             result = diffrenceAndPercentage(totalSum, totalSumPrev).Data

#             if totalSum == 0.0 and totalSumPrev == 0.0:
#                 continue

#             totalCurrentData += totalSum
#             totalPrevData += totalSumPrev

#             values.append(
#                 [
#                     key,
#                     str(totalSum),
#                     str(totalSumPrev),
#                     str(result["Diffrence"]),
#                     f"{result['PercentChange']}%",
#                 ]
#             )

#         totalValueresult = diffrenceAndPercentage(totalCurrentData, totalPrevData).Data

#         values.append(
#             [
#                 "Total Revenue",
#                 str(round(totalCurrentData, 2)),
#                 str(round(totalPrevData, 2)),
#                 str(totalValueresult["Diffrence"]),
#                 f"{totalValueresult['PercentChange']}%",
#             ]
#         )

#         tableObj = TableModel(
#             Title="Revneue Channels Comparison", Column=Headers, Rows=values
#         )

#         return Result(
#             Data=tableObj, Status=1, Message="Revenue Card calculated successfully"
#         )

#     except ZeroDivisionError as ex:
#         message = f"Error occurred at getFHSectionCards: {ex}"
#         print(f"{datetime.now()} {message}")
#         return Result(Data=None, Status=0, Message=message)

#     except Exception as ex:
#         message = f"Error occurred at getFHSectionCards: {ex}"
#         print(f"{datetime.now()} {message}")
#         return Result(Data=None, Status=0, Message=message)
