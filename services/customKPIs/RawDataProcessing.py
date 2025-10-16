from helper.FileUploadHandler import handleUploadFile
from core.models.base.ResultModel import Result
from services.customKPIs.FormatData import dataFormatting
from datetime import datetime
import os
from config.FilesBaseDIR import CUSTOM_KPIS_DATA_UPLOAD_DIR


def customKPIsDataProcessing(file, reportId: int) -> Result:
    try:
        # Create directory path based on report ID
        report_dir = os.path.join(CUSTOM_KPIS_DATA_UPLOAD_DIR, str(reportId))
        os.makedirs(report_dir, exist_ok=True)

        # Construct filename and extension
        file_name_only = f"CustomKPIs_{reportId}"
        file_extension = ".xlsx"  # or extract dynamically if needed

        # Save uploaded file inside the report-specific directory
        if file is not None:
            saved_file_path = handleUploadFile(
                file, file_name_only, file_extension, report_dir
            ).Data
        else:
            return Result(Status=0, Message="No file provided.")

        # Process the file after saving
        result = dataFormatting(saved_file_path,reportId)

        if result.Status == 1:
            response = {"CustomKPIs": result.Data["Custom KPIs"]}
            return Result(Data=response, Status=1, Message="File uploaded successfully.")

        # Remove file if incorrect format
        if os.path.exists(saved_file_path):
            os.remove(saved_file_path)

        return Result(Status=0, Message="Please upload the correct file format.")

    except Exception as e:
        return Result(Status=0, Message=f"Error: {str(e)}") 