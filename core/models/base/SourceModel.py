from pydantic import BaseModel,Field
from typing import Literal
from datetime import datetime
from typing import Optional,List
from enum import Enum


class SourceDataTypes(Enum):
    Actuals : str = "Actuals"
    Budget : str = "Budget"


class SourceMetaDataModel(BaseModel):
    SourceId : int
    ReportId : Optional[int] = None
    SourceType: Literal["Excel", "CSV", "API", "Database","Google Sheet"]
    SourceName: Optional[str] = Field(None, description="Name or identifier for the data source")
    FilePath: Optional[str] = Field(None, description="Local or cloud path to the file")
    SheetName: Optional[str] = Field(None, description="Applicable only for Excel files")
    TotalItems : int
    ItemsList : List[dict] 
    CreatedOn: Optional[datetime] = datetime.now()
    UpdatedOn: Optional[datetime] = datetime.now()
    UpdatedBy : Optional[int] = 1
    CreatedBy : Optional[int] = 1