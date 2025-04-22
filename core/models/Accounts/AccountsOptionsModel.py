from pydantic import BaseModel


class AccountOptions(BaseModel):
    KPIs: 1
    IncomeStatements: 2
