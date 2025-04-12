from helper.readExcel import readExcelFile
from datetime import datetime
from collections import defaultdict
from config.variable import variableMapping
from core.models.base.ResultModel import Result

# Analyze the data
def retriveAccountNames():
    try:
        filePath = "tempFiles/Honest Game Corporation Jan 2025 (4).xlsx"

        excelData = readExcelFile(filePath)

        data = excelData.Data

        result = defaultdict(dict)

        cleanedData = data[~data["Classification"].isnull()]


        for section , categories in variableMapping.items():

            for main,category in categories.items():
                
                for code in category:
                    
                    matches = cleanedData[
                        cleanedData["Classification"] == list(code.keys())[0]
                    ]

                    for _, row in matches.iterrows():

                        accountName = row["Account Name"]

                        matches = cleanedData[cleanedData["Account Name"] == accountName]

                        matches = matches.drop(columns=["Classification", "Account Name"])


                        result[main][accountName] = matches.iloc[0].to_dict()

        return Result(
            Data=result, Status=1, Message="Success"
        )

    except Exception as ex:
        message = f"Error occur at retriveAccountNames: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
