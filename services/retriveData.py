from helper.LoadJsonData import financialData,financialDataTest
from datetime import datetime
from core.models.base.ResultModel import Result

def getDataValues(mainSection:str,section:str, subSection:str, year=int, month=int):
    try:
        total = 0

        print(mainSection,section,subSection,"path")

        if month == 0:
            month = None
        
        data = financialData.get(mainSection, {}).get(section, {}).get(subSection, [])

        if month is None and year is None:
            total = 0
        else:
            for entry in data:
                if (year is None or entry.get("Year") == year) and (month is None or entry.get("Month") == month):
                    total += entry.get("Value", 0)

        return Result(Data=round(total,2), Status=1, Message="SUCCESS")

    except Exception as ex:
        message = f"Error occurred in get_data_values: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)


from helper.LoadJsonData import financialData
from datetime import datetime
from core.models.base.ResultModel import Result

def getTestValues(mainSection:str,section:str, subSection:str, year=int, month=int):
    try:
        total = 0

        # BalanceSheet ,CURRENT ASSETS ,Cash path

        if month == 0:
            month = None

        if mainSection == "Chart of Accounts":
            data = []

            # Check IncomeStatements first
            section_income = financialDataTest.get("IncomeStatements", {}).get(section, {})
            income_lineitems = section_income.get("LineItems", {})
            
            if subSection in income_lineitems:
                data = income_lineitems.get(subSection, [])
            else:
                # Fallback to BalanceSheet
                section_balance = financialDataTest.get("BalanceSheet", {}).get(section, {})
                balance_lineitems = section_balance.get("LineItems", {})
                data = balance_lineitems.get(subSection, [])

        else:
            data = financialDataTest.get(mainSection, {}).get(section, {}).get("Classification", {}).get(subSection,[])

        if month is None and year is None:
            total = 0
        else:
            for entry in data:
                if (year is None or entry.get("Year") == year) and (month is None or entry.get("Month") == month):
                    total += entry.get("Value", 0)

        return Result(Data=round(total,2), Status=1, Message="SUCCESS")

    except Exception as ex:
        message = f"Error occurred in get_data_values: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)

