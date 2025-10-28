from pydantic import BaseModel,Field
from typing import Literal
from datetime import datetime
from typing import Optional,List


class SourceModel(BaseModel):
    SourceType: Literal["Excel", "CSV", "API", "Database","Google Sheet"]
    SourceName: Optional[str] = Field(None, description="Name or identifier for the data source")
    FilePath: Optional[str] = Field(None, description="Local or cloud path to the file")
    SheetName: Optional[str] = Field(None, description="Applicable only for Excel files")
    UploadedAt: datetime = Field(default_factory=datetime.utcnow)
    UpdatedBy : int
    CreatedBy : int