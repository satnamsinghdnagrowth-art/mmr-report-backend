# Backend Financial Calculations - Detailed Documentation

This document provides comprehensive details of all financial calculations implemented in the backend system, including formulas, examples, file paths, and step-by-step logic.

---

## Table of Contents
1. [Revenue Calculations](#1-revenue-calculations)
2. [Profitability Metrics](#2-profitability-metrics)
3. [Expense Calculations](#3-expense-calculations)
4. [Earnings & EBIT](#4-earnings--ebit)
5. [Financial Ratios](#5-financial-ratios)
6. [Contribution Analysis](#6-contribution-analysis)
7. [Break-Even Analysis](#7-break-even-analysis)
8. [Cash Flow Activities](#8-cash-flow-activities)
9. [Balance Sheet Metrics](#9-balance-sheet-metrics)

---

## 1. Revenue Calculations

### 1.1 Total Revenue
**File Path:** `/backend/services/calculations/Revenue.py`  
**Function:** `totalRevenue(year, month, reportId, dataType)`

**Description:**  
Calculates the total revenue for a specified time period by summing all revenue entries.

**Logic Steps:**
1. Fetch financial data using `getFinancialData(reportId, dataType)`
2. Navigate to: `PROFIT & LOSS` → `REVENUE` → `Total`
3. Filter data where Year matches and Month is in the provided list
4. Sum all `Value` fields from filtered entries

**Formula:**
```
Total Revenue = Σ(Revenue Values for specified months)
```

**Example:**
```python
# Input Parameters
year = 2025
months = [1, 2, 3]  # Jan, Feb, Mar (Q1)
reportId = 12345

# Sample Data Structure:
[
    {"Year": 2025, "Month": 1, "Value": 50000},
    {"Year": 2025, "Month": 2, "Value": 55000},
    {"Year": 2025, "Month": 3, "Value": 60000}
]

# Calculation:
Total Revenue = 50000 + 55000 + 60000 = 165,000
```

**Return:** `Result(Data=165000.00, Status=1, Message="...")`

---

### 1.2 Revenue Growth
**File Path:** `/backend/services/calculations/Revenue.py`  
**Function:** `revenueGrowth(year, month, reportId, dataType)`

**Description:**  
Calculates Month-over-Month (MoM) or Quarter-over-Quarter (QoQ) revenue growth percentage.

**Logic Steps:**
1. **Determine Period Type:**
   - If `len(month) > 1`: Quarter mode
   - If `len(month) == 1`: Month mode

2. **Quarter Mode:**
   - Map months to quarters: Q1=[1,2,3], Q2=[4,5,6], Q3=[7,8,9], Q4=[10,11,12]
   - Find current quarter from provided months
   - Calculate previous quarter (Q1 → Q4 of previous year)
   
3. **Month Mode:**
   - Current month = month[0]
   - Previous month = month[0] - 1 (January → December of previous year)

4. Call `totalRevenue()` for current and previous periods
5. Calculate growth percentage

**Formula:**
```
Revenue Growth (%) = ((Current Period Revenue - Previous Period Revenue) / |Previous Period Revenue|) × 100
```

**Example - Month Mode:**
```python
# Input
year = 2025
months = [3]  # March

# Calculation
Current Month Revenue (Mar 2025) = 60,000
Previous Month Revenue (Feb 2025) = 55,000

Growth = ((60000 - 55000) / 55000) × 100 = 9.09%
```

**Example - Quarter Mode:**
```python
# Input
year = 2025
months = [1, 2, 3]  # Q1

# Calculation
Q1 2025 Revenue = 165,000
Q4 2024 Revenue = 150,000

Growth = ((165000 - 150000) / 150000) × 100 = 10.00%
```

**Return:** `Result(Data=10.00, Status=1, Message="...")`

---

## 2. Profitability Metrics

### 2.1 Gross Profit
**File Path:** `/backend/services/calculations/GrossProfit.py`  
**Function:** `grossProfit(year, month, reportId, dataType)`

**Description:**  
Calculates Gross Profit by subtracting direct expenses (cost of sales) from total revenue.

**Dependencies:**
- `Revenue.totalRevenue()`
- `Expenses.directExpenses()`

**Formula:**
```
Gross Profit = Total Revenue - Direct Expenses
```

**Example:**
```python
# Input
year = 2025
months = [1, 2, 3]

# Calculation
Total Revenue = 165,000
Direct Expenses (COGS) = 80,000

Gross Profit = 165000 - 80000 = 85,000
```

**Return:** `Result(Data=85000.00, Status=1, Message="...")`

---

### 2.2 Gross Profit Margin
**File Path:** `/backend/services/calculations/GrossProfit.py`  
**Function:** `grossProfitMargin(year, month, reportId, dataType)`

**Description:**  
Calculates Gross Profit as a percentage of total revenue.

**Formula:**
```
Gross Profit Margin (%) = (Gross Profit / Total Revenue) × 100
```

**Example:**
```python
Gross Profit = 85,000
Total Revenue = 165,000

GPM = (85000 / 165000) × 100 = 51.52%
```

**Return:** `Result(Data=51.52, Status=1, Message="...")`

---

### 2.3 Operating Profit
**File Path:** `/backend/services/calculations/GrossProfit.py`  
**Function:** `operatingProfit(year, month, reportId, dataType)`

**Description:**  
Calculates Operating Profit (EBIT before adjustments) by subtracting operating expenses from gross profit.

**Dependencies:**
- `GrossProfit.grossProfit()`
- `Expenses.totalOperatingExpenses()`

**Formula:**
```
Operating Profit = Gross Profit - Total Operating Expenses
```

**Example:**
```python
Gross Profit = 85,000
Operating Expenses = 45,000

Operating Profit = 85000 - 45000 = 40,000
```

**Return:** `Result(Data=40000.00, Status=1, Message="...")`

---

### 2.4 Net Income
**File Path:** `/backend/services/calculations/NetIncome.py`  
**Function:** `netIncome(year, month, reportId, dataType)`

**Description:**  
Calculates the bottom-line Net Income after all expenses including taxes.

**Dependencies:**
- `EarningBefore.earningBeforeTax()`

**Logic Steps:**
1. Get Earnings Before Tax (EBT)
2. Fetch Tax Expenses from: `PROFIT & LOSS` → `TAX EXPENSES` → `Tax Expense`
3. Filter tax data for specified period
4. Sum tax values
5. Subtract from EBT

**Formula:**
```
Net Income = Earnings Before Tax - Tax Expenses
```

**Example:**
```python
# Input
year = 2025
months = [1, 2, 3]

# Calculation
EBT = 35,000
Tax Expenses = 7,000

Net Income = 35000 - 7000 = 28,000
```

**Return:** `Result(Data=28000.00, Status=1, Message="...")`

---

### 2.5 Net Income Margin
**File Path:** `/backend/services/calculations/NetIncome.py`  
**Function:** `netIncomeMargin(year, month, reportId, dataType)`

**Description:**  
Calculates Net Income as a percentage of total revenue.

**Formula:**
```
Net Income Margin (%) = (Net Income / Total Revenue) × 100
```

**Example:**
```python
Net Income = 28,000
Total Revenue = 165,000

NIM = (28000 / 165000) × 100 = 16.97%
```

**Return:** `Result(Data=16.97, Status=1, Message="...")`

---

## 3. Expense Calculations

### 3.1 Direct Expenses (Cost of Sales)
**File Path:** `/backend/services/calculations/Expenses.py`  
**Function:** `directExpenses(year, month, reportId, dataType)`

**Description:**  
Calculates total cost of sales including both variable and fixed costs.

**Logic Steps:**
1. Fetch Variable Cost of Sales from: `PROFIT & LOSS` → `COST OF SALES` → `Variable Cost`
2. Filter and sum for specified period
3. Fetch Fixed Cost of Sales from: `PROFIT & LOSS` → `COST OF SALES` → `Fixed Cost`
4. Filter and sum for specified period
5. Add both components

**Formula:**
```
Direct Expenses = Variable Cost of Sales + Fixed Cost of Sales
```

**Example:**
```python
# Sample Data
Variable Cost of Sales:
- Jan: 15,000
- Feb: 16,000
- Mar: 17,000
Total VCOS = 48,000

Fixed Cost of Sales:
- Jan: 10,000
- Feb: 10,000
- Mar: 12,000
Total FCOS = 32,000

Direct Expenses = 48000 + 32000 = 80,000
```

**Return:** `Result(Data=80000.00, Status=1, Message="...")`

---

### 3.2 Total Operating Expenses
**File Path:** `/backend/services/calculations/Expenses.py`  
**Function:** `totalOperatingExpenses(year, month, reportId, dataType)`

**Description:**  
Calculates total operating expenses including variable, fixed, and depreciation.

**Logic Steps:**
1. Fetch Variable Expenses from: `PROFIT & LOSS` → `EXPENSES` → `Variable Expenses`
2. Fetch Fixed Expenses from: `PROFIT & LOSS` → `EXPENSES` → `Fixed Expenses`
3. Fetch Depreciation from: `PROFIT & LOSS` → `EXPENSES` → `Depreciation`
4. Sum all three components

**Formula:**
```
Operating Expenses = Variable Expenses + Fixed Expenses + Depreciation
```

**Example:**
```python
Variable Expenses = 18,000
Fixed Expenses = 20,000
Depreciation = 7,000

Operating Expenses = 18000 + 20000 + 7000 = 45,000
```

**Return:** `Result(Data=45000.00, Status=1, Message="...")`

---

### 3.3 Interest Expenses
**File Path:** `/backend/services/calculations/Expenses.py`  
**Function:** `interestExpenses(year, month, reportId, dataType)`

**Description:**  
Calculates total interest expenses paid on debt.

**Data Source:**  
`PROFIT & LOSS` → `INTEREST EXPENSES` → `Interest Expense`

**Formula:**
```
Interest Expenses = Σ(Interest Expense Values)
```

**Example:**
```python
Interest Expenses Q1 = 1,000 + 1,000 + 1,200 = 3,200
```

**Return:** `Result(Data=3200.00, Status=1, Message="...")`

---

### 3.4 Expenses to Revenue Ratio
**File Path:** `/backend/services/calculations/Expenses.py`  
**Function:** `expensesToRevenueRatio(year, month, reportId, dataType)`

**Description:**  
Calculates total expenses as a percentage of revenue.

**Dependencies:**
- `totalOperatingExpenses()`
- `directExpenses()`
- `totalRevenue()`

**Formula:**
```
Expense-to-Revenue Ratio (%) = ((Operating Expenses + Direct Expenses) / Total Revenue) × 100
```

**Example:**
```python
Operating Expenses = 45,000
Direct Expenses = 80,000
Total Revenue = 165,000

Total Expenses = 45000 + 80000 = 125,000
Ratio = (125000 / 165000) × 100 = 75.76%
```

**Return:** `Result(Data=75.76, Status=1, Message="...")`

---

## 4. Earnings & EBIT

### 4.1 EBIT (Earnings Before Interest & Tax)
**File Path:** `/backend/services/calculations/Ebit.py`  
**Function:** `EBIT(year, month, reportId, dataType)`

**Description:**  
Calculates EBIT by adjusting operating profit with other income and expenses.

**Dependencies:**
- `GrossProfit.operatingProfit()`
- `otherIncome()` (same file)
- `otherExpenses()` (same file)

**Logic Steps:**
1. Get Operating Profit
2. Get Other Income from: `PROFIT & LOSS` → `OTHER INCOME` → `Additional Income`
3. Get Other Expenses from: `PROFIT & LOSS` → `OTHER EXPENSES` → `Other Expenses`
4. Calculate EBIT

**Formula:**
```
EBIT = Operating Profit + Other Income - Other Expenses
```

**Example:**
```python
Operating Profit = 40,000
Other Income = 2,000
Other Expenses = 1,500

EBIT = 40000 + 2000 - 1500 = 40,500
```

**Return:** `Result(Data=40500.00, Status=1, Message="...")`

---

### 4.2 EBIT Margin
**File Path:** `/backend/services/calculations/Ebit.py`  
**Function:** `EBITMargin(year, month, reportId, dataType)`

**Description:**  
Calculates EBIT as a percentage of total revenue.

**Formula:**
```
EBIT Margin (%) = (EBIT / Total Revenue) × 100
```

**Example:**
```python
EBIT = 40,500
Total Revenue = 165,000

EBIT Margin = (40500 / 165000) × 100 = 24.55%
```

**Return:** `Result(Data=24.55, Status=1, Message="...")`

---

### 4.3 Earnings Before Tax (EBT)
**File Path:** `/backend/services/calculations/EarningBefore.py`  
**Function:** `earningBeforeTax(year, month, reportId, dataType)`

**Description:**  
Calculates earnings before tax by adjusting EBIT with interest income and expenses.

**Dependencies:**
- `Ebit.EBIT()`
- `OtherIncome.interestIncome()`

**Logic Steps:**
1. Get EBIT
2. Get Interest Income from: `PROFIT & LOSS` → `INTEREST INCOME` → `Interest Income`
3. Get Interest Expenses from: `PROFIT & LOSS` → `INTEREST EXPENSES` → `Interest Expense`
4. Calculate EBT

**Formula:**
```
EBT = EBIT + Interest Income - Interest Expenses
```

**Example:**
```python
EBIT = 40,500
Interest Income = 500
Interest Expenses = 3,200

EBT = 40500 + 500 - 3200 = 37,800
```

**Return:** `Result(Data=37800.00, Status=1, Message="...")`

---

## 5. Financial Ratios

### 5.1 Current Ratio
**File Path:** `/backend/services/calculations/Ratios.py`  
**Function:** `currentRatio(year, months, reportId, dataType)`

**Description:**  
Measures the company's ability to pay short-term obligations with current assets.

**Dependencies:**
- `CurrentAssestAndLiabilities.getTotalCurrentAssets()`
- `CurrentAssestAndLiabilities.getTotalCurrentLiabilities()`

**Logic Steps:**
1. Get Cash & Equivalents from: `BalanceSheet` → `CURRENT ASSETS` → `Cash & Equivalents`
2. Get Total Current Assets
3. Get Total Current Liabilities
4. Calculate ratio

**Formula:**
```
Current Ratio = (Total Current Assets + Cash & Equivalents) / Total Current Liabilities
```

**Example:**
```python
Cash & Equivalents = 30,000
Total Current Assets = 120,000
Total Current Liabilities = 60,000

Current Ratio = (120000 + 30000) / 60000 = 2.50
```

**Return:** `Result(Data=2.50, Status=1, Message="...")`

---

### 5.2 Cash Ratio
**File Path:** `/backend/services/calculations/Ratios.py`  
**Function:** `cashRatio(year, months, reportId, dataType)`

**Description:**  
Measures the company's ability to pay short-term obligations with only cash.

**Formula:**
```
Cash Ratio = Cash & Equivalents / Total Current Liabilities
```

**Example:**
```python
Cash & Equivalents = 30,000
Total Current Liabilities = 60,000

Cash Ratio = 30000 / 60000 = 0.50
```

**Return:** `Result(Data=0.50, Status=1, Message="...")`

---

### 5.3 Working Capital
**File Path:** `/backend/services/calculations/Ratios.py`  
**Function:** `workingCapital(year, months, reportId, dataType)`

**Description:**  
Calculates the difference between current assets and current liabilities.

**Formula:**
```
Working Capital = (Total Current Assets + Cash & Equivalents) - Total Current Liabilities
```

**Example:**
```python
Total Current Assets = 120,000
Cash & Equivalents = 30,000
Total Current Liabilities = 60,000

Working Capital = (120000 + 30000) - 60000 = 90,000
```

**Return:** `Result(Data=90000.00, Status=1, Message="...")`

---

## 6. Contribution Analysis

### 6.1 Contribution
**File Path:** `/backend/services/calculations/Contribution.py`  
**Function:** `contribution(year, month, reportId, dataType)`

**Description:**  
Calculates contribution margin (revenue minus all variable costs).

**Logic Steps:**
1. Get Total Revenue
2. Get Variable Cost of Sales from: `PROFIT & LOSS` → `COST OF SALES` → `Variable Cost`
3. Get Variable Expenses from: `PROFIT & LOSS` → `EXPENSES` → `Variable Expenses`
4. Calculate contribution

**Formula:**
```
Contribution = Total Revenue - Variable Cost of Sales - Variable Expenses
```

**Example:**
```python
Total Revenue = 165,000
Variable Cost of Sales = 48,000
Variable Expenses = 18,000

Contribution = 165000 - 48000 - 18000 = 99,000
```

**Return:** `Result(Data=99000.00, Status=1, Message="...")`

---

### 6.2 Contribution Margin
**File Path:** `/backend/services/calculations/Contribution.py`  
**Function:** `contributionMargin(year, month, reportId, dataType)`

**Description:**  
Calculates contribution as a percentage of revenue.

**Formula:**
```
Contribution Margin (%) = (Contribution / Total Revenue) × 100
```

**Example:**
```python
Contribution = 99,000
Total Revenue = 165,000

Contribution Margin = (99000 / 165000) × 100 = 60.00%
```

**Return:** `Result(Data=60.00, Status=1, Message="...")`

---

## 7. Break-Even Analysis

### 7.1 Break-Even Point
**File Path:** `/backend/services/calculations/BreakEvenMargin.py`  
**Function:** `breakEven(year, months, reportId, dataType)`

**Description:**  
Calculates the revenue level needed to cover all fixed costs.

**Dependencies:**
- `Contribution.contributionMargin()`

**Logic Steps:**
1. Get Fixed Expenses from: `PROFIT & LOSS` → `EXPENSES` → `Fixed Expenses`
2. Get Fixed Cost of Sales from: `PROFIT & LOSS` → `COST OF SALES` → `Fixed Cost`
3. Get Depreciation from: `PROFIT & LOSS` → `EXPENSES` → `Depreciation`
4. Get Contribution Margin (%)
5. Calculate break-even

**Formula:**
```
Break-Even Point = ((Fixed Expenses + Fixed Cost of Sales + Depreciation) / Contribution Margin (%)) × 100
```

**Example:**
```python
Fixed Expenses = 20,000
Fixed Cost of Sales = 32,000
Depreciation = 7,000
Contribution Margin = 60%

Total Fixed Costs = 20000 + 32000 + 7000 = 59,000

Break-Even = (59000 / 60) × 100 = 98,333.33
```

**Return:** `Result(Data=98333.33, Status=1, Message="...")`

---

### 7.2 Break-Even Margin of Safety
**File Path:** `/backend/services/calculations/BreakEvenMargin.py`  
**Function:** `breakEvenMarginSafety(year, months, reportId, dataType)`

**Description:**  
Calculates how much revenue exceeds the break-even point.

**Formula:**
```
Margin of Safety = Total Revenue - Break-Even Point
```

**Example:**
```python
Total Revenue = 165,000
Break-Even Point = 98,333.33

Margin of Safety = 165000 - 98333.33 = 66,666.67
```

**Return:** `Result(Data=66666.67, Status=1, Message="...")`

---

## 8. Cash Flow Activities

### 8.1 Operating Activities Cash Flow
**File Path:** `/backend/services/calculations/CashFlowActivities.py`  
**Function:** `getOperatingActivitiesCashFlow(year, months, reportId, dataType)`

**Description:**  
Calculates cash flow from operating activities using the indirect method.

**Logic Steps:**
1. Get Net Income
2. Add back Depreciation (non-cash expense)
3. Calculate Change in Current Assets (previous vs current period)
4. Calculate Change in Current Liabilities (current vs previous period)
5. Aggregate adjustments

**Formula:**
```
Operating Cash Flow = Net Income + Depreciation + Change in Current Liabilities + Change in Current Assets
```

**Example - Monthly:**
```python
Net Income (March) = 10,000
Depreciation (March) = 2,500

Current Assets (Feb) = 118,000
Current Assets (Mar) = 120,000
Change in CA = 118000 - 120000 = -2,000

Current Liabilities (Mar) = 62,000
Current Liabilities (Feb) = 60,000
Change in CL = 62000 - 60000 = 2,000

Operating CF = 10000 + 2500 + 2000 + (-2000) = 12,500
```

**Return:** `Result(Data=12500.00, Status=1, Message="...")`

---

### 8.2 Investing Activities Cash Flow
**File Path:** `/backend/services/calculations/CashFlowActivities.py`  
**Function:** `getInvestigatingActivitiesCashFlow(year, months, reportId, dataType)`

**Description:**  
Calculates cash flow from investing activities (asset purchases/sales).

**Logic Steps:**
1. Calculate change in Fixed Assets
2. Add back Depreciation (to get gross CAPEX)
3. Calculate change in Intangible Assets
4. Calculate change in Other Non-Current Assets
5. Aggregate all changes

**Formula:**
```
Investing CF = Change in Intangible Assets + Change in Other NCA + (Change in Fixed Assets - Depreciation)
```

**Example:**
```python
Fixed Assets (Feb) = 200,000
Fixed Assets (Mar) = 210,000
Change in FA = 200000 - 210000 = -10,000
Depreciation = 2,500
Net FA Change = -10000 - 2500 = -12,500

Intangible Assets Change = 0
Other NCA Change = 0

Investing CF = 0 + 0 + (-12500) = -12,500
```

**Return:** `Result(Data=-12500.00, Status=1, Message="...")`

---

### 8.3 Financing Activities Cash Flow
**File Path:** `/backend/services/calculations/CashFlowActivities.py`  
**Function:** `getFinancingActivitiesCashFlow(year, months, reportId, dataType)`

**Description:**  
Calculates cash flow from financing activities (equity and debt changes).

**Logic Steps:**
1. Calculate change in Other Equity
2. Calculate change in Retained Earnings
3. Adjust for current period net income (avoid double counting)
4. Aggregate changes

**Formula:**
```
Financing CF = Change in Other Equity + (Change in Retained Earnings - Net Income Adjustment)
```

**Example:**
```python
Other Equity (Mar) = 150,000
Other Equity (Feb) = 150,000
Change in OE = 0

Retained Earnings (Mar) = 85,000
Retained Earnings (Feb) = 75,000
Change in RE = 10,000

Net Income Adjustment = 0 (not January)

Financing CF = 0 + (10000 - 0) = 10,000
```

**Return:** `Result(Data=10000.00, Status=1, Message="...")`

---

## 9. Balance Sheet Metrics

### 9.1 Total Current Assets
**File Path:** `/backend/services/calculations/CurrentAssestAndLiabilities.py`  
**Function:** `getTotalCurrentAssets(year, months, reportId, dataType)`

**Description:**  
Calculates total current assets from balance sheet.

**Components:**
- Accounts Receivable: `BalanceSheet` → `CURRENT ASSETS` → `Accounts Receivable`
- Inventory: `BalanceSheet` → `CURRENT ASSETS` → `Inventory`
- Other Current Assets: `BalanceSheet` → `CURRENT ASSETS` → `Other Current Assets`

**Formula:**
```
Total Current Assets = Accounts Receivable + Inventory + Other Current Assets
```

**Example:**
```python
Accounts Receivable = 45,000
Inventory = 50,000
Other Current Assets = 25,000

Total CA = 45000 + 50000 + 25000 = 120,000
```

**Return:** `Result(Data=120000.00, Status=1, Message="...")`

---

### 9.2 Total Current Liabilities
**File Path:** `/backend/services/calculations/CurrentAssestAndLiabilities.py`  
**Function:** `getTotalCurrentLiabilities(year, months, reportId, dataType)`

**Description:**  
Calculates total current liabilities from balance sheet.

**Components:**
- Accounts Payable: `BalanceSheet` → `CURRENT LIABILITIES` → `Accounts Payable`
- Other Current Liabilities: `BalanceSheet` → `CURRENT LIABILITIES` → `Other Current Liabilities`

**Formula:**
```
Total Current Liabilities = Accounts Payable + Other Current Liabilities
```

**Example:**
```python
Accounts Payable = 35,000
Other Current Liabilities = 25,000

Total CL = 35000 + 25000 = 60,000
```

**Return:** `Result(Data=60000.00, Status=1, Message="...")`

---

## Data Source Structure

All calculations retrieve data from the consolidated financial data JSON structure via `helper/GetFinancialData.py`. The structure follows this hierarchy:

```json
{
  "PROFIT & LOSS": {
    "REVENUE": { "Total": [...], "Classification": {...} },
    "COST OF SALES": { "Classification": { "Variable Cost": [...], "Fixed Cost": [...] } },
    "EXPENSES": { "Classification": { "Variable Expenses": [...], "Fixed Expenses": [...], "Depreciation": [...] } },
    "INTEREST INCOME": { "Classification": { "Interest Income": [...] } },
    "INTEREST EXPENSES": { "Classification": { "Interest Expense": [...] } },
    "TAX EXPENSES": { "Classification": { "Tax Expense": [...] } },
    "OTHER INCOME": { "Classification": { "Additional Income": [...] } },
    "OTHER EXPENSES": { "Classification": { "Other Expenses": [...] } }
  },
  "BalanceSheet": {
    "CURRENT ASSETS": { "Classification": { "Cash & Equivalents": [...], "Accounts Receivable": [...], "Inventory": [...] } },
    "CURRENT LIABILITIES": { "Classification": { "Accounts Payable": [...], "Other Current Liabilities": [...] } },
    "NON-CURRENT ASSETS": { "Classification": { "Fixed Assets": [...], "Intangible Assets": [...] } }
  },
  "EQUITY": {
    "EQUITY": { "Classification": { "Other Equity": [...], "Retained Earnings": [...], "Current Earnings": [...] } }
  }
}
```

Each data array contains objects with:
```json
{
  "Year": 2025,
  "Month": 3,
  "Value": 15000.00
}
```

---

## Error Handling

All calculation functions implement consistent error handling:

1. **ZeroDivisionError**: Returns `Result(Data=0, Status=0, Message="...")` with error details
2. **Exception**: Catches all other errors, logs with timestamp, returns `Result(Status=0, Message="...")`
3. **Logging**: Prints errors to console with `datetime.now()` timestamp

**Example Error Response:**
```python
Result(
    Data=0,
    Status=0,
    Message="Error occurred at totalRevenue: division by zero"
)
```

---

## Calculation Dependencies Map

```
Net Income
├── earningBeforeTax
│   ├── EBIT
│   │   ├── operatingProfit
│   │   │   ├── grossProfit
│   │   │   │   ├── totalRevenue
│   │   │   │   └── directExpenses
│   │   │   └── totalOperatingExpenses
│   │   ├── otherIncome
│   │   └── otherExpenses
│   └── interestIncome
└── Tax Expenses (direct fetch)
```

This hierarchical dependency ensures that each metric builds upon previously calculated values, maintaining consistency throughout the financial reporting system.
