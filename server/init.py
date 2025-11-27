from fastapi import FastAPI
from routes.dataAnalyze import ReportRouter
from routes.formatData import UploadRouter
from routes.AccountElements import AccountItemsRouter
from routes.FinancialHighligths import FinancialHighlights
from routes.ProfitablitySection import ProfitAbility
from routes.ExpensesAnalysis import ExpensesAnalysis
from routes.BreakEvenAnalysis import BreakEvenAnaysis
from routes.CashFlowAnalysis import CashFlow
from routes.BudgetSection import BudgetSectionRouter
from routes.FullSectionRouter import ConsolidateSectionsData
from fastapi.staticfiles import StaticFiles
from routes.CustomKpis import CustomKPIsRouter
from routes.authentication.User import UserRouter
from routes.authentication.Role import RoleRouter
from routes.SummaryGeneration import SummaryGeneratorRouter
from routes.ReportProgressHandling import ReportProgressRouter

# App Instance
app = FastAPI()
1
# Data Preprccessing Routes
app.include_router(UploadRouter, prefix="/api/v1/upload/file")
app.include_router(ReportRouter, prefix="/api/v1/report")
app.include_router(AccountItemsRouter, prefix="/api/v1/Account")

# Authentication Routes
app.include_router(RoleRouter, prefix="/api/v1/role")
app.include_router(UserRouter, prefix="/api/v1/authentication")

# Summary Generation Routes
app.include_router(SummaryGeneratorRouter, prefix="/api/v1/summary/generation")

# Sections Routes
app.include_router(ConsolidateSectionsData, prefix="/api/v1/section/Data")
app.include_router(FinancialHighlights, prefix="/api/v1/section/financialHighlights")
app.include_router(ProfitAbility, prefix="/api/v1/section/profitability")
app.include_router(ExpensesAnalysis, prefix="/api/v1/section/expensesAnalysis")
app.include_router(BreakEvenAnaysis, prefix="/api/v1/section/breakEvenAnalysis")
app.include_router(CashFlow, prefix="/api/v1/section/cashflowAnalysis")
app.include_router(BudgetSectionRouter, prefix="/api/v1/section/budgetComparison")

# Custom KPI Routes
app.include_router(CustomKPIsRouter, prefix="/api/v1/customskpis")

# Report Progress Route
app.include_router(ReportProgressRouter, prefix="/api/v1/progress")

# Static Files handling
app.mount("/database", StaticFiles(directory="database"), name="company_assets")