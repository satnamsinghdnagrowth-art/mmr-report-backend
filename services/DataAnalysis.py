# from helper.readExcel import readExcelFile
# from datetime import datetime
# from services.calculations.revenueCalculation import calculateRevenue
# from services.calculations.monthlyValues import calculateMonthlyValues
# from core.models.base.ResultModel import Result

# # Analyze the data
# def analyze():
#     try:
#         filePath = "tempFiles/Honest Game Corporation Jan 2025 (4).xlsx"

#         excelData = readExcelFile(filePath)

#         data = excelData.Data

#         result = calculateMonthlyValues(data)

#         # data.to_dict(orient="records")

#         return Result(Data=result.Data, Status=1, Message="Success")

#     except Exception as ex:
#         message = f"Error occur at readExcelFile: {ex}"
#         print(f"{datetime.now()} {message}")
#         return Result(Status=0, Message=message)
