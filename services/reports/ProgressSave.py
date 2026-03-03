from datetime import datetime
import os
import json

from core.models.base.ResultModel import Result
from config.FilesBaseDIR import REPORT_META_DATA_JSON_PATH, CUSTOM_KPIS_DATA_UPLOAD_DIR
from helper.SaveCustomKpisList import CustomKpisList

def _sync_custom_kpis(reportId: int, metaData: dict):
    """
    Remove any custom KPIs from customKpisData.json that are no longer
    referenced in the saved layout (e.g. user deleted the visual or the whole page).
    """
    try:
        kpi_path = f"{CUSTOM_KPIS_DATA_UPLOAD_DIR}/{reportId}/customKpisData.json"
        if not os.path.exists(kpi_path):
            return

        with open(kpi_path, "r", encoding="utf-8") as f:
            existing_kpis = json.load(f)

        if not isinstance(existing_kpis, list) or not existing_kpis:
            return

        # Extract all visual IDs currently in the saved layout or in the unassigned pool
        saved_layout_ids = set()
        for page in metaData.get("pages", []):
            category = page.get("category", {})
            for vt in ["Cards", "Charts", "Tables"]:
                for item in category.get(vt, []):
                    # item might be a string ID or dict. Handle both
                    vid = item.get("Id") if isinstance(item, dict) else item
                    if vid:
                        saved_layout_ids.add(vid)
                        
        # Also preserve unassigned visuals so they don't get deleted from disk
        unassigned = metaData.get("unassigned", {})
        for vt in ["Cards", "Charts", "Tables"]:
            for vid in unassigned.get(vt, []):
                saved_layout_ids.add(vid)

        # Filter out custom KPIs that have a VisualId but it's not in the saved layout NOR unassigned pool
        original_count = len(existing_kpis)
        updated_kpis = []
        for entry in existing_kpis:
            visual_id = entry.get("CustomKpi", {}).get("VisualId")
            
            # If it has a generated VisualId AND it's not tracked anywhere, it's orphaned -> drop it
            if visual_id and visual_id not in saved_layout_ids:
                continue
                
            updated_kpis.append(entry)

        # If any were orphaned, write the cleaned list back to disk and clear cache
        if len(updated_kpis) < original_count:
            with open(kpi_path, "w", encoding="utf-8") as f:
                json.dump(updated_kpis, f, indent=4)
            CustomKpisList.pop(reportId, None)
            print(f"{datetime.now().isoformat()} | _sync_custom_kpis: Removed {original_count - len(updated_kpis)} orphaned custom KPIs for report {reportId}")

    except Exception as ex:
        print(f"Error syncing custom KPIs during layout save: {ex}")


def reportProgressSave(metaData: dict) -> Result:
    try:
        reportId = metaData.get("reportId")
        if not reportId:
            return Result(Status=0, Message="reportId is missing in metaData")

        # Sync/cleanup orphaned custom KPIs before saving layout
        _sync_custom_kpis(reportId, metaData)

        # Ensure directory exists
        os.makedirs(REPORT_META_DATA_JSON_PATH, exist_ok=True)

        file_path = os.path.join(REPORT_META_DATA_JSON_PATH, f"{reportId}.json")

        # Save JSON safely
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(
                metaData,
                f,
                indent=4,
                default=str  # handles datetime or other non-serializable objects
            )

        return Result(Status=1, Message="Executive Summary Saved Successfully")

    except Exception as ex:
        message = f"Error occurred at reportProgressSave: {ex}"
        print(f"{datetime.now().isoformat()} | {message}")
        return Result(Data=None, Status=0, Message=message)

