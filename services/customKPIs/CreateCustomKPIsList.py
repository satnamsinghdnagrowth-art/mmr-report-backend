from core.models.base.ResultModel import Result
import json
import os
import traceback
from datetime import datetime
from helper.SaveCustomKpisList import getCustomKpisList, CustomKpisList
from config.FilesBaseDIR import CUSTOM_KPIS_DATA_UPLOAD_DIR
from core.models.base.SectionNamesEnum import get_section_id
from helper.GenerateVisualId import generate_visual_id

REPORT_JSON_PATH = "database/ReportTable.json"


def addCustomKPI(reportId: int, payload) -> Result:
    try:
        # Auto-populate SectionId if not provided
        kpi_dict = payload.dict()
        if not kpi_dict.get("SectionId"):
            kpi_dict["SectionId"] = get_section_id(kpi_dict["SectionName"])

        # Pre-generate the VisualId that ConsolidateDataReporting will produce
        # so that the DELETE endpoint can match by this ID later.
        visual_type = str(kpi_dict.get("VisualType", "")).lower()
        filtered_stub = {"Report Id": reportId, "Custom KPIs": {item: [] for item in (kpi_dict.get("Items") or [])}}
        payload_params = {"Items": kpi_dict.get("Items"), "VisualType": kpi_dict.get("VisualType")}
        kpi_dict["VisualId"] = generate_visual_id(visual_type, filtered_stub, payload_params)

        customReportData = {
            "ReportId": reportId,
            "CustomKpi": kpi_dict
        }

        print(customReportData)

        report_json_path = (
            f"{CUSTOM_KPIS_DATA_UPLOAD_DIR}/{reportId}/customKpisData.json"
        )

        # Ensure directory exists
        os.makedirs(os.path.dirname(report_json_path), exist_ok=True)

        # Load existing data safely
        existing_data = []
        if os.path.exists(report_json_path):
            try:
                with open(report_json_path, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
                    if not isinstance(existing_data, list):
                        existing_data = []
            except json.JSONDecodeError:
                existing_data = []

        # Return existing entry if same VisualType + Items already registered (prevent duplicates)
        for entry in existing_data:
            if entry.get("ReportId") == reportId:
                existing_kpi = entry.get("CustomKpi", {})
                if (existing_kpi.get("VisualType") == kpi_dict.get("VisualType") and
                        sorted(existing_kpi.get("Items") or []) == sorted(kpi_dict.get("Items") or [])):
                    return Result(Data=entry, Status=1, Message="KPI already registered.")

        # Append new KPI data
        existing_data.append(customReportData)

        # Save updated data to disk
        with open(report_json_path, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=4)

        # ── Invalidate in-memory cache so the next sectionData call re-reads
        # from disk and picks up this newly added custom KPI. ──
        CustomKpisList.pop(reportId, None)

        return Result(
            Data=customReportData,
            Status=1,
            Message="KPI added successfully."
        )

    except Exception as ex:
        error_trace = traceback.format_exc()
        message = f"Error occurred in customKPICreation: {ex}"

        print(f"{datetime.now()} {message}")
        print(error_trace)

        return Result(
            Status=0,
            Message=message
        )
