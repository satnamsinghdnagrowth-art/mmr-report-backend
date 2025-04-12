from pydantic import BaseModel


class ReportDescriptionsModel(BaseModel):
    ReportName : str
    FinancialYear : str
    DataRange : list[str]
