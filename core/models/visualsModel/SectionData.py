from pydantic import BaseModel
from typing import Optional, List
from core.models.visualsModel.CardModel import CardDataModel
from core.models.visualsModel.ChartModel import ChartDataModel
from core.models.visualsModel.TableModel import TableModel


class SectionData(BaseModel):
    Cards: List[CardDataModel]
    Charts: List[ChartDataModel]
    Tables: List[TableModel]
