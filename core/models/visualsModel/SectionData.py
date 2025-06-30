from pydantic import BaseModel
from typing import Optional, List
from core.models.visualsModel.CardModel import CardDataModel
from core.models.visualsModel.ChartModel import ChartDataModel
from core.models.visualsModel.TableModel import TableModel


class SectionData(BaseModel):
    Cards: Optional[List[CardDataModel]] = []
    Charts: Optional[List[ChartDataModel]] = []
    Tables: Optional[List[TableModel]] = []
