# YTD Calculation Fix - Based on Financial Year Start

## Summary
Fixed the YTD (Year-To-Date) calculation in the INCOME_STATEMENT_TABLE to use the Financial Year Start month from the Excel file instead of hardcoded values.

## Changes Made

### File Modified
**`backend/services/reportSection/financialHighlights/tables/IncomeStatementTablesKPI.py`**

### What Was Fixed

#### Before:
Lines 96-108 had hardcoded values for margin calculations:
```python
if entry["func"] == "grossProfitMargin":
    ytdValue = func(
        year=2025,
        month=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        reportId=reportId,
    ).Data
elif entry["func"] == "netIncomeMargin":
    ytdValue = func(
        year=2025,
        month=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        reportId=reportId,
    ).Data
```

#### After:
Lines 95-139 now dynamically calculate based on Financial Year:
```python
if entry["func"] == "grossProfitMargin" or entry["func"] == "netIncomeMargin":
    # Group months by year for proper calculation
    year_month_map = {}
    for y, m in ytd_months:
        if y not in year_month_map:
            year_month_map[y] = []
        year_month_map[y].append(m)
    
    # Calculate margin for each year and then aggregate
    if len(year_month_map) == 1:
        # All months in same year
        year_val = list(year_month_map.keys())[0]
        months_val = year_month_map[year_val]
        ytdValue = func(
            year=year_val,
            month=months_val,
            reportId=reportId,
        ).Data
    else:
        # Cross-year: calculate weighted average
        total_months = len(ytd_months)
        weighted_margin = 0
        for year_val, months_val in year_month_map.items():
            margin = func(
                year=year_val,
                month=months_val,
                reportId=reportId,
            ).Data
            weight = len(months_val) / total_months
            weighted_margin += margin * weight
        ytdValue = weighted_margin
```

## How It Works

### 1. Financial Year Configuration
The Financial Year Start is read from the Excel file:
- **Excel Cell A2**: "Financial Year Start:"
- **Excel Cell B2**: Month name (e.g., "January", "July")
- **Stored in JSON**: As month number (1-12) in `Report Details.Financial Year`

### 2. YTD Calculation Logic
The code at lines 80-93 already had the correct logic to calculate YTD months:

**Same Calendar Year** (e.g., FY starts in Jan, current month is Oct):
- Include: Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct
- Total: 10 months

**Spanning Calendar Years** (e.g., FY starts in Jul, current month is Jan):
- Include: Jul, Aug, Sep, Oct, Nov, Dec (previous year) + Jan (current year)
- Total: 7 months

### 3. What Was Fixed
The margin calculations (Gross Profit Margin, Net Income Margin) were using hardcoded values instead of the dynamically calculated `ytd_months` list. This has been corrected to use the proper YTD period.

## Test Results

### Test Case 1: Financial Year = 7 (July), Current Month = October 2025

**Report ID**: 75222
**Company**: Chicken Barn Limited

**Expected YTD Months**: July, August, September, October (4 months)

**Results**:
```
Revenue YTD: $3,907,472.43
  - Jul 2025: $1,051,105.23
  - Aug 2025: $965,998.06
  - Sep 2025: $900,357.74
  - Oct 2025: $990,011.40
✅ Total: $3,907,472.43 (Verified)
```

### Test Case 2: Financial Year = 1 (January), Current Month = October 2025

**Report ID**: 30712
**Company**: Hey Bagel, LLC

**Expected YTD Months**: Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct (10 months)

**Results**:
```
Revenue YTD: $1,052,333.79
  - Jan-Jun 2025: $0.00 (no data)
  - Jul 2025: $0.00
  - Aug 2025: $343,099.30
  - Sep 2025: $378,028.90
  - Oct 2025: $331,205.59
✅ Total: $1,052,333.79 (Verified)
```

### Test Case 3: Cross-Year Scenario

**Scenario**: Financial Year = 7 (July), Current Month = January 2026

**Expected YTD Months**: Jul, Aug, Sep, Oct, Nov, Dec (2025) + Jan (2026) = 7 months

**Verification**:
```python
# Simulation test passed
Actual YTD Months (from logic):
  - Jul 2025
  - Aug 2025
  - Sep 2025
  - Oct 2025
  - Nov 2025
  - Dec 2025
  - Jan 2026
✅ Correct! 7 months calculated for cross-year scenario
```

## API Testing

**Endpoint**: `POST /api/v1/section/financialHighlights/get/report/{reportId}/sectionData/`

**Request Payload**:
```json
{
  "Year": 2025,
  "Months": [10],
  "ReportType": "Month",
  "SectionName": "Financial Heights"
}
```

**Response** (Excerpt):
```json
{
  "Data": {
    "Tables": [
      {
        "Id": "INCOME_STATEMENT_TABLE",
        "Title": "Income Statement",
        "Column": [
          "Particulars",
          "Oct 2025",
          "Sep 2025",
          "This Month vs Last Month(%)",
          "This Month vs Last Month($)",
          "2025 (YTD)"
        ],
        "Rows": [
          [
            {"Value": "Revenue", ...},
            {"Value": 990011.40, "Type": "currency", "Symbol": "$"},
            {"Value": 900357.74, "Type": "currency", "Symbol": "$"},
            {"Value": 9.96, "Type": "percentage", "Symbol": "%"},
            {"Value": 89653.66, "Type": "currency", "Symbol": "$"},
            {"Value": 3907472.43, "Type": "currency", "Symbol": "$"}
          ]
        ]
      }
    ]
  }
}
```

## Files Created for Testing

1. **`backend/test_ytd_calculation.py`** - API endpoint testing script
2. **`backend/verify_ytd_logic.py`** - Detailed YTD calculation verification script

## Verification Checklist

- [x] YTD calculation reads Financial Year from Report Details
- [x] YTD correctly calculates for same calendar year scenarios
- [x] YTD correctly calculates for cross-year scenarios
- [x] Margin calculations (Gross Profit Margin, Net Income Margin) use dynamic YTD
- [x] Regular KPI calculations (Revenue, COGS, etc.) sum correctly over YTD period
- [x] API returns correct YTD values in response
- [x] Test scripts created and verified
- [x] No hardcoded year or month values remain

## Impact

This fix ensures that:
1. YTD calculations respect the company's actual financial year
2. Reports are accurate regardless of when the financial year starts
3. Cross-year financial periods (e.g., July-June) are handled correctly
4. All calculations (revenue, expenses, margins) use consistent YTD periods

## Notes

- The server is running on `http://192.168.29.85:8081`
- No server restart required (Python file changes are auto-detected)
- The fix maintains backward compatibility with existing data
