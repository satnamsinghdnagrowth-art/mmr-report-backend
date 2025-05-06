from services.calculations.Revenue import totalRevenue, revenueGrowth
from services.calculations.GrossProfit import grossProfit, grossProfitMargin
from services.calculations.NetProfit import netProfit, netProfitMargin
from services.calculations.Ebit import EBIT, EBITMargin
from services.calculations.NetIncome import netIncome, netIncomeMargin
from services.calculations.Expenses import expensesToRevenueRatio
from services.calculations.OtherIncome import otherIncome, interestIncome
from services.calculations.EarningBefore import (
    earningBeforeInterestandTax,
    earningBeforeTax,
)
from services.calculations.Expenses import directExpenses, totalOperatingExpenses


functionRegistry = {
    "totalRevenue": totalRevenue,
    "grossProfit": grossProfit,
    "grossProfitMargin": grossProfitMargin,
    "directExpenses": directExpenses,
    "totalOperatingExpenses": totalOperatingExpenses,
    "netProfit": netProfit,
    "netProfitMargin": netProfitMargin,
    "ebit": EBIT,
    "ebitMargin": EBITMargin,
    "otherIncome": otherIncome,
    "interestIncome": interestIncome,
    "earningBeforeInterestandTax": earningBeforeInterestandTax,
    "earningBeforeTax": earningBeforeTax,
    "netIncome": netIncome,
    "netIncomeMargin": netIncomeMargin,
    "revenueGrowth": revenueGrowth,
    "expensesToRevenueRatio":expensesToRevenueRatio
}
