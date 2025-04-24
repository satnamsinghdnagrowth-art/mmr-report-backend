from pydantic import BaseModel
from typing import List, Optional


class DateFilter(BaseModel):
    Year: Optional[int] = None
    Month: Optional[List[int]] = None
