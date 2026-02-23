# Year Display Fixes for Variance Tables

## Quick Summary
Fixed 4 table files that were showing incorrect years when comparing months across year boundaries (e.g., Jan 2026 vs Dec 2025).

## Problem
All tables were showing: `Jan 2026` vs `Dec 2026` (both 2026)  
Should show: `Jan 2026` vs `Dec 2025` (correct years)

## Root Cause
Using fixed `year` parameter instead of dynamic `currentYear` and `prevYear` values from `getCurrentAndPreviousPeriods()` function.

## Files Fixed

### 1. services/reportSection/detailedSheet/cashFlowTable.py
**Line 50**: Changed `{year}` to `{y}` to use actual year from staticMonths tuple

### 2. services/reportSection/financialHighlights/tables/IncomeStatementTablesKPI.py
**Lines 55-56**: Changed both columns to use `currentYear` and `prevYear`

### 3. services/reportSection/financialHighlights/tables/RevenueBreakDown.py  
**Lines 38-39**: Changed both columns to use `currentYear` and `prevYear`

### 4. services/reportSection/profitAbility/tables/GetProfitAbilityTable.py
**Lines 47-48**: Changed both columns to use `currentYear` and `prevYear`

## Pattern Applied
```python
# BEFORE (Wrong):
Headers = [
    "Particulars",
    f"{calendar.month_abbr[currentMonths[0]]} {year}",  # ❌
    f"{calendar.month_abbr[prevMonths[0]]} {year}",     # ❌
    ...
]

# AFTER (Correct):
Headers = [
    "Particulars", 
    f"{calendar.month_abbr[currentMonths[0]]} {currentYear}",  # ✅
    f"{calendar.month_abbr[prevMonths[0]]} {prevYear}",        # ✅
    ...
]
```

## Affected APIs
- Income Statement variance table
- Revenue Channels Comparison table  
- Profitability Analysis variance table
- Cash Flow Statement table

## Testing
Verified with Report 30712 (data spans Aug 2025 - Jan 2026):
- ✅ Income Statement: Shows "Jan 2026" and "Dec 2025"
- ✅ Cash Flow: Shows "Aug 2025", "Sep 2025", "Oct 2025", "Nov 2025", "Dec 2025", "Jan 2026"

## Deployment
**Required**: Backend server restart for changes to take effect.

---
**Date**: 2026-02-13  
**Issue**: Incorrect years in variance table headers  
**Status**: Fixed ✅
