from pydantic import BaseModel
from typing import Optional, List
from core.models.visualsModel.CardModel import CardDataModel
from core.models.visualsModel.ChartModel import ChartDataModel
from core.models.visualsModel.TableModel import TableModel


# Section Data
class SectionData(BaseModel):
    Cards: Optional[List[CardDataModel]] = []
    Charts: Optional[List[ChartDataModel]] = []
    Tables: Optional[List[TableModel]] = []


# Consolidate Section
class ConsolidateSectionDate(BaseModel):
    SectionName: str
    SectionData: SectionData
    Visbility: Optional[bool] = True


class SectionDataModel(BaseModel):
    Sections : List[ConsolidateSectionDate] 