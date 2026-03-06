from helper.FileUploadHandler import handleUploadFile
from core.models.base.ResultModel import Result
from services.customKPIs.FormatData import dataFormatting
from config.FilesBaseDIR import CUSTOM_KPIS_DATA_UPLOAD_DIR
from datetime import datetime
import os


def customKPIsDataProcessing(file, reportId) -> Result:
    try:
        reportId = int(reportId)

        # Save uploaded Excel file under the report-specific directory
        report_dir = os.path.join(CUSTOM_KPIS_DATA_UPLOAD_DIR, str(reportId))
        os.makedirs(report_dir, exist_ok=True)

        if file is None:
            return Result(Status=0, Message="No file provided.")

        saved_file_path = handleUploadFile(
            file, f"CustomKPIs_{reportId}", ".xlsx", report_dir
        ).Data

        # Process Excel → write CustomFile_{reportId}.json
        result = dataFormatting(saved_file_path, reportId)

        if result.Status != 1:
            # Remove the unusable Excel file on format errors
            if saved_file_path and os.path.exists(saved_file_path):
                os.remove(saved_file_path)
            return result   # forward the descriptive error message

        kpi_names = list(result.Data.get("Custom KPIs", {}).keys())
        return Result(
            Data={"CustomKPIs": kpi_names},
            Status=1,
            Message=f"File uploaded successfully. {len(kpi_names)} custom KPI(s) found.",
        )

    except Exception as e:
        print(f"{datetime.now()} Error in customKPIsDataProcessing: {e}")
        return Result(Status=0, Message=f"Error: {str(e)}")
