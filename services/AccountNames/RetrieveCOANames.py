from helper.readExcel import readExcelFile
from datetime import datetime
from collections import defaultdict
from helper.getMonthName import getMonthName
from config.variable import variableMapping
from core.models.base.ResultModel import Result


# Analyze the data
def retriveCOANames(year,month):
    try:
        filePath = "tempFiles/Honest Game Corporation Jan 2025 (4).xlsx"

        excelData = readExcelFile(filePath)

        data = excelData.Data

        result = defaultdict(dict)

        cleanedData = data[~data["Classification"].isnull()]

        for section, categories in variableMapping.items():
            for main, category in categories.items():
                for code in category:
                    
                    matches = cleanedData[
                            cleanedData["Classification"] == list(code.keys())[0]
                        ]

                    for _, row in matches.iterrows():
                        accountName = row["Account Name"]

                        monthly_totals = [
                            {
                                "Label": f"This Month-{getMonthName(month)} {year}",
                                "Month": month,
                                "Year": year,
                            },
                            {
                                "Label": f"Next Month-{getMonthName(month + 1)} {year}",
                                "Month": month + 1,
                                "Year": year,
                            },
                            {
                                "Label": f"Prev Month-{getMonthName(month - 1)} {year}",
                                "Month": month - 1,
                                "Year": year,
                            },
                            {"Label": f"This Year-{year}", "Month": 0, "Year": year},
                            {"Label": f"Next Year-{year + 1}", "Month": 0, "Year": year + 1},
                            {"Label": f"Prev Year {year - 1}", "Month": 0, "Year": year - 1},
                        ]


                        # matches = cleanedData[
                        #     cleanedData["Account Name"] == accountName
                        # ]

                        # matches = matches.drop(
                        #     columns=["Classification", "Account Name"]
                        # )

                        result[main][accountName] = monthly_totals

        return Result(Data=result, Status=1, Message="Success")

    except Exception as ex:
        message = f"Error occur at retriveAccountNames: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
