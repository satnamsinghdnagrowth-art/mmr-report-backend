from fastapi import APIRouter
from services.reportSection.financialHeights.SectionData import getSectionData
from services.reportSection.financialHeights.cardsKPIs import getSectionCards
from services.reportSection.financialHeights.chartsKPIs import getSectionCharts
from services.reportSection.financialHeights.IncomeStatementTablesKPI import getISTable

visual = APIRouter()

@visual.get("/get/financialHeights/")
def getCards():
    return getSectionData(year=2024,months=[1,2,3,4,5,6,7,8,9,10,11,12],reportType="Yearly",section="Financial Heights")

@visual.get("/get/financialHeights/cards")
def getCards():
    return getSectionCards(year=2024,months=[1,2,3,4,5,6,7,8,9,10,11,12],reportType="Yearly",section="Financial Heights")

@visual.get("/get/financialHeights/charts")
def getCards():
    return getSectionCharts(year=2024,months=[1,2,3,4,5,6,7,8,9,10,11,12],reportType="Yearly",section="Financial Heights")


@visual.get("/get/financialHeights/tables")
def getCharts():
    return getISTable(year=2024,months=[1,2,3,4,5,6,7,8,9,10,11,12],reportType="Yearly",section="Financial Heights")



