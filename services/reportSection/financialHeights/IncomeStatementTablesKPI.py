from datetime import datetime
from core.models.base.ResultModel import Result
from helper.LoadJsonData import SECTION_CARD_CONFIGS
from services.calculations.Revenue import totalRevenue
from services.calculations.Expenses import directExpenses,totalOperatingExpenses
from services.calculations.GrossProfit import grossProfit,grossProfitMargin
from services.calculations.DiffrenceCalculation import diffrenceAndPercentage
from core.models.visualsModel.TableModel import TableModel
from services.reportSection.financialHeights.tables.RevenueBreakDown import getRevenueTable
from config.FunctionMaping import functionRegistry
from datetime import datetime

# Get the sections cards
def getISTable(year:int,months:list[int],reportType:str,section:str):
    try:
        configs = SECTION_CARD_CONFIGS.get(section)

        if not configs:
            return Result(Data=[], Status=1, Message=f"No cards configured for section '{section}'")

        tables = []
    
        for config in configs.get("tables"):
            Headers = config["columns"]

            rows = []
        
            for entry in config["rows"]:
                row = [entry["label"]]
                func = functionRegistry.get(entry["func"])
                
                thisMonthValue = func(year=year, month=months).Data
                prevMonthValue = func(year=year-1, month=months).Data
                
                row.append(str(thisMonthValue))
                row.append(str(prevMonthValue))
                
                result = diffrenceAndPercentage(thisMonthValue, prevMonthValue).Data
                
                row.append(str(result["Diffrence"]))
                row.append(f"{result["PercentChange"]}%")
                
                rows.append(row)
            
                # Create TableModel and return result
            tableObj = TableModel(Title="Income Statement", Column=Headers, Rows=rows)

            tables.append(tableObj)

        tables.append(getRevenueTable(year,months).Data)

        

        return Result(
            Data=tables,
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
    
