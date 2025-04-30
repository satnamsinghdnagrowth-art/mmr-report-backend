from datetime import datetime
from core.models.base.ResultModel import Result
from helper.LoadJsonData import SECTION_CARD_CONFIGS
from core.models.visualsModel.TableModel import TableModel
from helper.LoadJsonData import financialDataTest
from services.calculations.DiffrenceCalculation import diffrenceAndPercentage
from config.FunctionMaping import functionRegistry
from datetime import datetime

# Get the sections cards
def getRevenueTable(year:int,months):
    try:

        revenueData = financialDataTest["PROFIT & LOSS"]["REVENUE"]["LineItems"]

        Headers = ["REVENUE","2024","2023","This Year VS Prev Year($)","Variance"]

        values = []

        totalCurrentData = 0
        totalPrevData = 0

        for key,data in revenueData.items():


            filteredDataCurrent = [ entry for entry in data if entry['Year'] == year and entry['Month'] in months
            ]

            totalSum = sum(item["Value"] for item in filteredDataCurrent)

            filteredDataPrev = [ entry for entry in data if entry['Year'] == year-1 and entry['Month'] in months
            ]
                
            totalSumPrev = sum(item["Value"] for item in filteredDataPrev)

            result = diffrenceAndPercentage(totalSum, totalSumPrev).Data

            if totalSum == 0.0 and totalSumPrev == 0.0:
                continue


            totalCurrentData += totalSum
            totalPrevData += totalSumPrev

            values.append([key,str(totalSum),str(totalSumPrev),str(result["Diffrence"]),f"{result["PercentChange"]}%"])

        totalValueresult = diffrenceAndPercentage(totalCurrentData, totalPrevData).Data
        
        values.append([
            "Total Revenue",
            str(round(totalCurrentData, 2)),
            str(round(totalPrevData, 2)),str(totalValueresult["Diffrence"]),f"{totalValueresult["PercentChange"]}%"
            ])

        tableObj = TableModel(Title = "Revneue Channels Comparison",Column=Headers,Rows=values)

        return Result(
            Data=tableObj,
            Status=1,
            Message="Revenue Card calculated successfully"
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at getFHSectionCards: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occurred at getFHSectionCards: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
    
