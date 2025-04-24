from fastapi import FastAPI
from routes.dataAnalyze import Analyze
from routes.formatData import dataFormat
from routes.AccountElements import Account

app = FastAPI()


app.include_router(dataFormat, prefix="/api/v1/format")
app.include_router(Analyze, prefix="/api/v1/dataAnalysis")
app.include_router(Account, prefix="/api/v1/Account")
