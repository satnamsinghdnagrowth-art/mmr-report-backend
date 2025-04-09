from fastapi import FastAPI
from routes.dataAnalyze import Analyze
from routes.getAccountNames import Account

app = FastAPI()

app.include_router(Analyze,prefix="/api/v1/dataAnalysis")
app.include_router(Account, prefix="/api/v1/Account")
app.include_router(Account, prefix="/api/v1/Account")


app.include_router(Account, prefix="/api/v1/Account")




