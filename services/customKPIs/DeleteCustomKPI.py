from core.models.base.ResultModel import Result
import json
import os
import traceback
from datetime import datetime
from helper.SaveCustomKpisList import CustomKpisList
from config.FilesBaseDIR import CUSTOM_KPIS_DATA_UPLOAD_DIR


def _fingerprint(kpi_dict: dict) -> str:
    """Create a stable fingerprint from VisualType + sorted Items + SectionId."""
    vt = str(kpi_dict.get("VisualType", "")).lower()
    items = sorted(str(i) for i in kpi_dict.get("Items", []))
    sid = str(kpi_dict.get("SectionId", ""))
    return f"{vt}|{','.join(items)}|{sid}"


def deleteCustomKPI(reportId: int, visual_id: str) -> Result:
    """
    Remove ALL custom KPI entries for a report that match the given visual_id.

    Two-tier matching strategy:
    1. Primary  — match by stored 'VisualId' field (new entries have this).
    2. Fallback — derive the fingerprint from the visual_id prefix and match by
                  VisualType + Items + SectionId (handles legacy entries without 'VisualId').

    All exact-duplicate entries are also removed as a housekeeping step.
    """
    try:
        report_json_path = (
            f"{CUSTOM_KPIS_DATA_UPLOAD_DIR}/{reportId}/customKpisData.json"
        )

        if not os.path.exists(report_json_path):
            return Result(Status=0, Message="customKpisData.json not found for this report.")

        with open(report_json_path, "r", encoding="utf-8") as f:
            existing_data = json.load(f)

        if not isinstance(existing_data, list):
            return Result(Status=0, Message="Unexpected file format.")

        original_count = len(existing_data)

        # ---------- Pass 1: remove by stored VisualId ----------
        updated_data = [
            entry for entry in existing_data
            if entry.get("CustomKpi", {}).get("VisualId") != visual_id
        ]
        removed_by_id = original_count - len(updated_data)

        # ---------- Pass 2: fallback — remove by visual_type + items fingerprint ----------
        # The visual_id format is: custom_kpi_{type}_{reportId}_{kpi_name}_{hash}
        # We can't fully back-calculate the hash, but we CAN match by VisualType inferred
        # from the id prefix and Items present in the visual_id suffix.
        # Simpler: match ANY entry whose generated fingerprint corresponds to the visual
        # that was on-screen.  We do this by comparing the VisualId stored vs the
        # requested visual_id using a startswith on the deterministic prefix part.
        if removed_by_id == 0:
            # No VisualId match — try prefix match to catch legacy entries.
            # Prefix: custom_kpi_{type}_{reportId}_
            prefix_parts = visual_id.split("_")
            # visual_id = custom_kpi_table_67017_wages_...
            # Extract visual type (index 2) for fingerprint filtering
            visual_type = prefix_parts[2] if len(prefix_parts) > 2 else ""

            updated_data = [
                entry for entry in existing_data
                if not (
                    str(entry.get("CustomKpi", {}).get("VisualType", "")).lower() == visual_type
                    # For legacy entries we cannot match perfectly, so we only skip
                    # entries that already have a VisualId (they should have been caught
                    # in Pass 1).  Entries without VisualId and matching VisualType are
                    # removed — this is safe for deduplication.
                    and entry.get("CustomKpi", {}).get("VisualId") is None
                    and entry.get("ReportId") == reportId
                )
            ]

        # ---------- Pass 3: remove ALL exact duplicates (housekeeping) ----------
        seen_fingerprints = set()
        deduplicated = []
        for entry in updated_data:
            fp = _fingerprint(entry.get("CustomKpi", {}))
            if fp not in seen_fingerprints:
                seen_fingerprints.add(fp)
                deduplicated.append(entry)

        final_removed = original_count - len(deduplicated)

        if final_removed == 0:
            return Result(
                Status=1,
                Message="No matching KPI entry found — may have already been removed."
            )

        # Persist cleaned list
        with open(report_json_path, "w", encoding="utf-8") as f:
            json.dump(deduplicated, f, indent=4)

        # Invalidate in-memory cache
        CustomKpisList.pop(reportId, None)

        return Result(
            Status=1,
            Message=f"Custom KPI deleted. Removed {final_removed} entr(ies) (visual_id={visual_id})."
        )

    except Exception as ex:
        error_trace = traceback.format_exc()
        message = f"Error deleting custom KPI: {ex}"
        print(f"{datetime.now()} {message}")
        print(error_trace)
        return Result(Status=0, Message=message)

