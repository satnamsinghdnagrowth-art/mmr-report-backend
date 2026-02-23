# Balance Sheet Table Fixes - Complete Documentation

## Issues Fixed

### **CRITICAL: Two Separate Implementations Found!**

The system had **TWO different files** generating Balance Sheet tables:
1. `BS_Table.py` - Used by some sections
2. `table.py` - Used by Cash Flow Analysis section (**getDetailedTable** function)

**Both files had the same bugs and both needed fixes!**

---

### 1. **Empty staticMonths Bug** (Critical)
**Problem**: All detailed sheet tables (BS_Table, PNL_Table, cashFlowTable, table.py) were generating an empty `staticMonths` list, resulting in tables with no data rows.

**Root Cause**: The logic was trying to generate months by counting backwards from `(max(months), year)`, but:
- `year` parameter is the fiscal year (e.g., 2026)
- Actual data months span across years (e.g., Aug 2025 - Jan 2026)
- So it was looking for `(12, 2026), (11, 2026), etc.` but data had `(12, 2025), (11, 2025), etc.`

**Fix**: Instead of generating months from parameters, use actual months from Excel data:
```python
# BEFORE (Lines 34-44 in all files):
staticMonths = []
current_month = max(months)
current_year = year
for _ in range(6):
    if (current_month, current_year) in available_months_set:
        staticMonths.insert(0, (current_month, current_year))
    current_month -= 1
    if current_month == 0:
        current_month = 12
        current_year -= 1

# AFTER:
staticMonths = available_months[-6:] if len(available_months) >= 6 else available_months
```

**Files Fixed**:
- `services/reportSection/detailedSheet/BS_Table.py` (Lines 19-24)
- `services/reportSection/detailedSheet/PNL_Table.py` (Lines 26-31)
- `services/reportSection/detailedSheet/cashFlowTable.py` (Lines 26-32)
- `services/reportSection/detailedSheet/table.py` (Lines 31-39) ⭐ **NEW**

---

### 2. **Duplicate Row Names in Balance Sheet**
**Problem**: Items appeared twice with same names:
```json
Row: "Cash & Equivalents" (0 values) ← Subsection header
Row: "Cash & Equivalents" (6 values) ← Actual data (DUPLICATE!)
```

**Root Cause**: The code structure was:
1. Add subsection header (e.g., "Cash & Equivalents")
2. Loop through items in subsection
3. Add item rows (including "Cash & Equivalents" as item name)

When the subsection name matched the only item name, it created duplicates.

**Fix**: Skip subsection header when there's only ONE item with the SAME name as the subsection:

```python
# Check if subsection has only one item with same name
item_names = list(subSectionContent.keys())
skip_subsection_header = (
    len(subSectionRows) == 1 and 
    len(item_names) == 1 and 
    item_names[0] == subSectionName
)

# Add subsection header only if not a duplicate name
if not skip_subsection_header:
    subsectionHeader = [ValueObjectModel(Value=subSectionName, ...)]
    subSectionRows.insert(0, subsectionHeader)
```

**Files Fixed**: 
- `services/reportSection/detailedSheet/BS_Table.py` (Lines 93-164)
- `services/reportSection/detailedSheet/table.py` (Lines 134-218) ⭐ **NEW**

**Examples Fixed**:
- "Cash & Equivalents" - subsection with 1 item of same name → no duplicate
- "Accounts Payable" - subsection with 1 item of same name → no duplicate  
- "Retained Earnings" - subsection with 1 item of same name → no duplicate
- "Other Current Assets" - subsection with multiple items → keeps header

---

### 3. **Empty Sections Appearing**
**Problem**: Subsections with no data (e.g., "Accounts Receivable", "Inventory") were showing as empty header rows.

**Root Cause**: Subsection headers were added BEFORE checking if any items had data.

**Fix**: Only add subsection headers and totals when `grandTotal != 0`:
```python
grandTotal = sum(monthlyTotals.values())
if grandTotal != 0.0:
    # Add subsection header, items, and total ONLY if there's data
    ...
```

Already implemented in both BS_Table.py and table.py.

---

## Variance Table Year Fixes (Previous Issue)

**Problem**: Tables showing same year for both periods (e.g., "Jan 2026" vs "Dec 2026")

**Fix**: Use `currentYear` and `prevYear` from `getCurrentAndPreviousPeriods()` instead of `year` parameter.

**Files Fixed**:
- `services/reportSection/detailedSheet/cashFlowTable.py` (Line 50)
- `services/reportSection/financialHighlights/tables/IncomeStatementTablesKPI.py` (Lines 55-56)
- `services/reportSection/financialHighlights/tables/RevenueBreakDown.py` (Lines 38-39)
- `services/reportSection/profitAbility/tables/GetProfitAbilityTable.py` (Lines 47-48)

---

## Summary of Changes

### Files Modified (7 total):

1. **BS_Table.py**
   - Fixed staticMonths generation (use Excel data)
   - Skip duplicate subsection headers
   - Lines changed: 19-24, 93-164

2. **table.py** ⭐ **NEW FIX**
   - Fixed staticMonths generation (use Excel data)
   - Skip duplicate subsection headers
   - Lines changed: 31-39, 134-218
   - **Note**: This file is used by Cash Flow Analysis section!

3. **PNL_Table.py**
   - Fixed staticMonths generation (use Excel data)
   - Lines changed: 26-31

4. **cashFlowTable.py**
   - Fixed staticMonths generation (use Excel data)
   - Fixed year display in headers
   - Lines changed: 26-32, 50

5-7. **Variance tables** (IncomeStatementTablesKPI, RevenueBreakDown, GetProfitAbilityTable)
   - Use currentYear/prevYear instead of year
   - Lines changed: 38-48, 55-56

---

## Where Each File Is Used

- **BS_Table.py** → Used by: financialHighlights, expensesAnalysis, profitAbility sections
- **table.py** → Used by: **Cash Flow Analysis section** (SectionDataCF.py)
- **PNL_Table.py** → Used by various sections for P&L tables
- **cashFlowTable.py** → Used by Cash Flow Analysis for cash flow statements

---

## Testing Results

### Balance Sheet Table (Report 30712) - Both Implementations
✅ **BS_Table.py**:
   - Headers: `['BalanceSheet', 'Aug 2025', ..., 'Jan 2026']`
   - 44 rows, no duplicates

✅ **table.py** (getDetailedTable):
   - Headers: `['BALANCE SHEET', 'Aug 2025', ..., 'Jan 2026']`
   - 44 rows, no duplicates

### Profit & Loss Table (Report 30712)
✅ Headers: `['PROFIT & LOSS', 'Aug 2025', ..., 'Jan 2026', 'Total']`  
✅ 59 rows generated  

### Cash Flow Statement (Report 30712)
✅ Headers: `['CashFlow Statements', 'Aug 2025', ..., 'Jan 2026']`  
✅ 19 rows generated  

---

## API Endpoint
All fixes apply to: `http://192.168.29.85:8081/api/v1/section/Data/get/report/{reportId}/sectionData/`

---

## Next Steps
1. ⚠️ **RESTART BACKEND SERVER** to apply all changes
2. **Clear Python cache** if needed:
   ```bash
   find . -type d -name "__pycache__" -exec rm -rf {} +
   find . -name "*.pyc" -delete
   ```
3. Test API endpoint with Report 30712
4. Verify Balance Sheet no longer has:
   - Duplicate "Cash & Equivalents", "Accounts Payable", etc.
   - Empty sections with no data
5. Verify all month headers show correct years (Aug 2025 - Jan 2026)

---

**Date**: 2026-02-13  
**Issue**: Balance Sheet duplicates and empty staticMonths (TWO files affected!)  
**Status**: Fixed ✅ (Both BS_Table.py AND table.py)

