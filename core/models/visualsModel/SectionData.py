from pydantic import BaseModel
from typing import Optional, List
from core.models.visualsModel.CardModel import CardDataModel
from core.models.visualsModel.ChartModel import ChartDataModel
from core.models.visualsModel.TableModel import TableModel


# ── Internal models (used for data processing / persistence) ─────────────────

class SectionData(BaseModel):
    """Raw visual data for one section — used internally and for saving."""
    Cards: Optional[List[CardDataModel]] = []
    Charts: Optional[List[ChartDataModel]] = []
    Tables: Optional[List[TableModel]] = []


class ConsolidateSectionDate(BaseModel):
    """Full section record with nested visuals — used internally only."""
    SectionId: str
    SectionName: str
    SectionData: SectionData
    Visbility: Optional[bool] = True


class SectionDataModel(BaseModel):
    """Persisted snapshot — full sections with nested visuals."""
    Sections: List[ConsolidateSectionDate]


# ── API-facing models ─────────────────────────────────────────────────────────

class SectionMeta(BaseModel):
    """
    Lean section descriptor returned in the API response.
    Visuals are NOT nested here — they live in the flat
    Cards / Charts / Tables pools at the top level, each stamped
    with SectionID, PageNo, and Order for easy grouping on the frontend.
    """
    SectionId: str
    SectionName: str
    PageNo: int
    Visibility: Optional[bool] = True


class CombinedSectionResponse(BaseModel):
    """
    Single API payload combining:
      - Sections: ordered list of lean section metadata (no redundant visual data)
      - Cards / Charts / Tables: flat pools, each item stamped with
        SectionID, PageNo, Order so the frontend can reconstruct page layout.
    """
    Sections: List[SectionMeta] = []
    Cards: List[CardDataModel] = []
    Charts: List[ChartDataModel] = []
    Tables: List[TableModel] = []


# Legacy flat model kept for backward compatibility
class FlatSectionData(BaseModel):
    Cards: List[CardDataModel] = []
    Charts: List[ChartDataModel] = []
    Tables: List[TableModel] = []
