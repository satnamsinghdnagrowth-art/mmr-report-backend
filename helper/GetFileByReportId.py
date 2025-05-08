import json
from typing import Optional
import os

report_data = {}

def getFileNameByReportId(reportId: int, filePath: str = "database\ReportTable.json") -> Optional[str]:
    try:
        with open(filePath, "r") as f:
            raw_data = json.load(f)

        data = {str(k): v for k, v in raw_data.items()}

        print(reportId,"dfgjdf")

        print()

        return data.get(str(reportId), {}).get("FileName")
    
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        return None


def getReportData(reportId: int):
    

    if reportId not in report_data:
        print("fetched Once")
        fileName = getFileNameByReportId(reportId)

        if not fileName:
            raise ValueError(f"No file name found for report ID {reportId}")

        folderPath = "database/reportsDataFiles"
        filePath = os.path.join(folderPath, fileName)

        if not os.path.exists(filePath):
            raise FileNotFoundError(f"Report file not found at: {filePath}")

        with open(filePath, "r") as f:
            report_data[reportId] = json.load(f)
    print("fetched Not again")

    return report_data[reportId]
