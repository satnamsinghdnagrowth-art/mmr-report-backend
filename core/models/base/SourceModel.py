from pydantic import BaseModel
from typing import Literal


class SourceModel(BaseModel):
    SourceName : Literal["Excel","Connector"]
    