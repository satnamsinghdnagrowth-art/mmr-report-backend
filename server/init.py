from fastapi import FastAPI
from routes.dataAnalyze import Analyze
from routes.formatData import dataFormat
from routes.AccountElements import Account
from routes.reportVisual import visual

app = FastAPI()

# Routes Prefix
app.include_router(dataFormat, prefix="/api/v1/format")
app.include_router(Analyze, prefix="/api/v1/dataAnalysis")
app.include_router(Account, prefix="/api/v1/Account")
app.include_router(visual, prefix="/api/v1/visual")
