from fastapi import FastAPI
from routes.dataAnalyze import Analyze
from routes.formatData import dataFormat
from routes.AccountElements import Account
from routes.FinancialHighligths import FinancialHighlights
from routes.ProfitablitySection import ProfitAbility
from routes.ExpensesAnalysis import ExpensesAnalysis
from routes.BreakEvenAnalysis import BreakEvenAnaysis

app = FastAPI()

# Routes Prefix
app.include_router(dataFormat, prefix="/api/v1/format")
app.include_router(Analyze, prefix="/api/v1/dataAnalysis")
app.include_router(Account, prefix="/api/v1/Account")

# Sections Routes
app.include_router(FinancialHighlights, prefix="/api/v1/section/financialHighlights")
app.include_router(ProfitAbility, prefix="/api/v1/section/profitability")
app.include_router(ExpensesAnalysis, prefix="/api/v1/section/expensesAnalysis")
app.include_router(BreakEvenAnaysis, prefix="/api/v1/section/breakEvenAnalysis")
