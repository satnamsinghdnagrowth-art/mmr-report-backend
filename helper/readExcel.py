import pandas as pd
from datetime import datetime
from core.models.base.ResultModel import Result

# Read the excel File
def readExcelFile(filepath)->Result:
    try:
        df = pd.read_excel(filepath, header=4)

        return Result(Data=df, Status=0, Message="SUCCESS")
    
    except Exception as ex:
        message = f"Error occur at readExcelFile: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)