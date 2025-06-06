import json
from typing import Optional
import os

report_data = {}

Report_Table_File_Path = os.path.join("database", "ReportTable.json")


def getFileNameByReportId(reportId: int) -> Optional[str]:
    try:
        with open(Report_Table_File_Path, "r") as f:
            reports = json.load(f)

        print(type(reportId))

        for report in reports:
            if report.get("ReportId") == int(reportId):
                return report.get("FileName")

        return None  # Not found

    except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        return None



def getReportData(reportId: int,reportDetail:Optional[bool]= False):
    if reportId not in report_data:
        fileName = getFileNameByReportId(reportId)


        if not fileName:
            raise ValueError(f"No file name found for report ID {reportId}")

        folderPath = os.path.join("database", "reportsDataFiles")
        filePath = os.path.join(folderPath, fileName)

        if not os.path.exists(filePath):
            raise FileNotFoundError(f"Report file not found at: {filePath}")

        try:
            with open(filePath, "r") as f:
                data = json.load(f)
                
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in report file: {filePath}")
        
        report_data[reportId] = data

    return report_data[reportId]
