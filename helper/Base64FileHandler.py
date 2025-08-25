from datetime import datetime
from core.models.base.ResultModel import Result
import os
import base64
from services.accountValues.GetFinancialsValues import formatFinancialData
from config.FilesBaseDIR import UPLOAD_DIR


def handleBase64File(base64str: str, fileNameOnly: str, fileExtension: str):
    try:
        try:
            header, encoded = (
                base64str.split(",", 1) if "," in base64str else ("", base64str)
            )
            decoded_bytes = base64.b64decode(encoded)

        except Exception:
            return Result(Status=0, Message="Invalid base64 string provided.")

        timeStamp = datetime.now().strftime(
            "%Y%m%d%H%M%S"
        )  # Format timestamp for filename safety

        savedFileName = f"{fileNameOnly}_{timeStamp}{fileExtension}"
        filePath = os.path.join(UPLOAD_DIR, savedFileName)

        with open(filePath, "wb") as f:
            f.write(decoded_bytes)

        return Result(
            Data=filePath,
            Status=1,
            Message="Total contribution calculated successfully",
        )

    except Exception as ex:
        message = f"Error occur at getValueSum: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
