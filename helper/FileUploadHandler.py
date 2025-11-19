from datetime import datetime
from core.models.base.ResultModel import Result
import os, shutil, traceback

def handleUploadFile(file, fileNameOnly: str, fileExtension: str, UPLOAD_DIR: str):
    try:
        UPLOAD_DIR = os.path.abspath(UPLOAD_DIR)
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        timeStamp = datetime.now().strftime("%Y%m%d%H%M%S")

        if fileExtension.lower() not in [".xlsx", ".xls"]:
            return Result(Status=0, Message="Please upload an Excel file.")

        savedFileName = f"{fileNameOnly}_{timeStamp}{fileExtension}"
        filePath = os.path.join(UPLOAD_DIR, savedFileName)

        # Reset pointer before reading
        file.file.seek(0)

        # Write file to disk
        with open(filePath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"✅ File saved at: {filePath}")

        return Result(
            Data=filePath,
            Status=1,
            Message="File Uploaded Successfully",
        )

    except Exception as ex:
        print(traceback.format_exc())
        message = f"Error occur at handleUploadFile: {ex}"
        return Result(Status=0, Message=message)
