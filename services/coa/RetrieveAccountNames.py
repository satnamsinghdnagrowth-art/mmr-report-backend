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

        result = defaultdict(list)

        cleanedData = data[~data["Classification"].isnull()]

        for section , categories in variableMapping.items():

            for main,category in categories.items():
                
                for code in category:
                    
                    matches = cleanedData[
                        cleanedData["Classification"] == list(code.keys())[0]
                    ]

                    for _, row in matches.iterrows():
                        result[main].append(
                            { "name": row["Account Name"]}
                        )

        return Result(
            Data=result, Status=1, Message="Success"
        )

    except Exception as ex:
        message = f"Error occur at readExcelFile: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
