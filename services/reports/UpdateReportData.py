from datetime import datetime
from config.FilesBaseDIR import REPORT_JSON_PATH
from core.models.base.ResultModel import Result
from helper.LoadJsonData import SECTION_CARD_CONFIGS
from services.visuals.card.retrieveCard import retrieveCard
from datetime import datetime
import os
import json
from config.FilesBaseDIR import PROGRESS_JSON_PATH
from helper.GetFileByReportId import getReportMetaDatabyId
import shutil


# Get the sections cards
def updateReportFields(reportId: int, companyLogo):
    try:
        # Load all reports
        with open(REPORT_JSON_PATH, "r") as file:
            reports = json.load(file)

        # Find the specific report
        report = None
        for r in reports:
            if r["ReportId"] == reportId:
                report = r
                break

        if not report:
            return Result(Status=0, Message="Report not found.")

        # Save logo file
        logoFileName = f"logo_{reportId}"
        fileExtension = ".png"
        timeStamp = datetime.now().strftime("%Y%m%d%H%M%S")
        savedFileName = f"{logoFileName}_{timeStamp}{fileExtension}"
        logoFilePath = os.path.join("database/companyLogos", savedFileName)

        with open(logoFilePath, "wb") as buffer:
            shutil.copyfileobj(companyLogo.file, buffer)

        # Update report field
        report["CompanyLogoFilePath"] = logoFilePath

        # Save all reports back to the file
        with open(REPORT_JSON_PATH, "w") as file:
            json.dump(reports, file, indent=4)

        response = {
            "CompanyLogoPath":logoFilePath
        }

        return Result(Data=response,Status=1, Message="Uploaded successfully")

    except Exception as ex:
        message = f"Error occurred at updateReportFields: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
