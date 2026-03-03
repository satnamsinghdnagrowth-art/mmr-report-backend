from fastapi import FastAPI
from routes.dataAnalyze import ReportRouter
from routes.formatData import UploadRouter
from routes.AccountElements import AccountItemsRouter
from routes.FinancialHighligths import FinancialHighlightsRouter
from routes.ProfitablitySection import ProfitAbilityRouter
from routes.ExpensesAnalysis import ExpensesAnalysisRouter
from routes.BreakEvenAnalysis import BreakEvenAnaysisRouter
from routes.CashFlowAnalysis import CashFlowRouter
from routes.BudgetSection import BudgetSectionRouter
from routes.FullSectionRouter import ConsolidateDataRouter
from fastapi.staticfiles import StaticFiles
from routes.CustomKpis import CustomKPIsRouter
from routes.authentication.User import UserRouter
from routes.authentication.Role import RoleRouter
from routes.SummaryGeneration import SummaryGeneratorRouter
from routes.ReportProgressHandling import ReportProgressRouter
from routes.Templates import TemplatesRouter

# App Instance
app = FastAPI()

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
app.include_router(ConsolidateDataRouter, prefix="/api/v1/section/Data")
app.include_router(FinancialHighlightsRouter, prefix="/api/v1/section/financialHighlights")
app.include_router(ProfitAbilityRouter, prefix="/api/v1/section/profitability")
app.include_router(ExpensesAnalysisRouter, prefix="/api/v1/section/expensesAnalysis")
app.include_router(BreakEvenAnaysisRouter, prefix="/api/v1/section/breakEvenAnalysis")
app.include_router(CashFlowRouter, prefix="/api/v1/section/cashflowAnalysis")
app.include_router(BudgetSectionRouter, prefix="/api/v1/section/budgetComparison")

# Custom KPI Routes
app.include_router(CustomKPIsRouter, prefix="/api/v1/customskpis")

# Report Progress Route
app.include_router(ReportProgressRouter, prefix="/api/v1/progress")

# Templates Route
app.include_router(TemplatesRouter, prefix="/api/v1/templates")

# Static Files handling
app.mount("/database", StaticFiles(directory="database"), name="company_assets")