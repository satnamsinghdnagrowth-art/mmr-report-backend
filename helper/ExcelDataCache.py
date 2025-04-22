from helper.readExcel import readExcelFile

_exceldata = None

filePath = "tempFiles/Honest Game Corporation Jan 2025 (4).xlsx"


def load_excel():
    global _exceldata
    _exceldata = readExcelFile(filePath)


def get_excel_data():
    return _exceldata
