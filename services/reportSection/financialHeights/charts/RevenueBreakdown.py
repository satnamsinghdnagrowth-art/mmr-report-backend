from datetime import datetime
from core.models.base.ResultModel import Result
from helper.LoadJsonData import SECTION_CARD_CONFIGS
from core.models.visualsModel.ChartModel import ChartDataModel,YAxisSeriesModel
from helper.LoadJsonData import financialDataTest
from services.calculations.DiffrenceCalculation import diffrenceAndPercentage
from config.FunctionMaping import functionRegistry
from datetime import datetime
from typing import List

# Get the sections cards
def getRevenueBreakdownChart(year:int ,months:list[int]):
    try:
        revenueData = financialDataTest["PROFIT & LOSS"]["REVENUE"]["LineItems"]

        xAxis = []

        yAxis = []

        for key,data in revenueData.items():

            filteredDataCurrent = [ entry for entry in data if entry['Year'] == year and entry['Month'] in months
            ]

            totalSum = sum(item["Value"] for item in filteredDataCurrent)

            if totalSum == 0.0 :
                continue

            yAxis.append(totalSum)
            xAxis.append(key)

        yAxisObj = YAxisSeriesModel(Title="Revenue",Type="bar",Values = yAxis)
            
        chartObj = ChartDataModel(Title = "Revenue BreakDown",Xaxis=xAxis,YaxisSeries=[yAxisObj],IndexAxis="y")
          
        return Result(
            Data=chartObj,
            Status=1,
            Message="Revenue chart calculated successfully"
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at getRevenueBreakdownChart: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occurred at getRevenueBreakdownChart: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
    
