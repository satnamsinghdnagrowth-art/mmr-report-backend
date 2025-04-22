
from helper.readExcel import readExcelFile
from datetime import datetime
from collections import defaultdict
from config.variable import variableMapping
from core.models.base.ResultModel import Result


# Analyze the data
def testformat():
    try:
        filePath = "tempFiles/Live_Productions_Australia_Pty_Ltd_-_Balance_Sheet.xlsx"

        excelData = readExcelFile(filePath)

        df = excelData.Data

        data = df[~(df["Account"].isnull() & df["Unnamed: 0"].isnull())]

        cleanedData = data.rename(columns = {"Unnamed: 0":"Category"})

        cleanedData = cleanedData.fillna(0)

        structured_output = []
        current_category = None

        for row in cleanedData.to_dict(orient="records") :
          
            category = row["Category"]
            account = row["Account"]

            # if account == 0 :
            #     continue

            # If category is not 0, start a new category group
            if category != 0:
                current_category = {
                    "Category": category,
                    "Accounts": []
                }
                structured_output.append(current_category)

            
            account_data = {k: v for k, v in row.items() if k != "Category" }
            current_category["Accounts"].append(account_data)


        return Result(Data=structured_output, Status=1, Message="Success")

    except Exception as ex:
        message = f"Error occur at retriveBSAccountNames: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
