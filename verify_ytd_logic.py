#!/usr/bin/env python3
"""
Detailed verification of YTD calculation logic
"""
import sys
sys.path.insert(0, '/home/hello/Work/MMR_Report_Generation/backend')

from helper.GetFileByReportId import getReportData
from services.calculations.Revenue import totalRevenue

# Test with report ID 75222
reportId = 75222

# Get report data
financialData = getReportData(reportId)["Report Details"]
financialMonth = financialData["Financial Year"]

print("=" * 80)
print("YTD Calculation Verification")
print("=" * 80)
print(f"\nReport ID: {reportId}")
print(f"Company: {financialData['Company Name']}")
print(f"Financial Year Start: Month {financialMonth} ({['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][financialMonth-1]})")

# Simulate the YTD calculation for October 2025
currentYear = 2025
currentMonths = [10]  # October

latest_month = currentMonths[0]
ytd_months = []

if latest_month >= financialMonth:
    # Same year: financialMonth to latest_month
    for m in range(financialMonth, latest_month + 1):
        ytd_months.append((currentYear, m))
else:
    # Across two years: (finMonth to Dec of last year) + (Jan to latest_month)
    for m in range(financialMonth, 13):
        ytd_months.append((currentYear - 1, m))
    for m in range(1, latest_month + 1):
        ytd_months.append((currentYear, m))

print(f"\nCurrent Month: {latest_month} (October 2025)")
print(f"\nYTD Calculation Logic:")
print(f"  Financial Year Start: {financialMonth}")
print(f"  Current Month: {latest_month}")
print(f"  Logic: latest_month ({latest_month}) >= financialMonth ({financialMonth}): {latest_month >= financialMonth}")

month_names = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

print(f"\nYTD Months Included (Total: {len(ytd_months)}):")
for year, month in ytd_months:
    print(f"  - {month_names[month]} {year}")

# Calculate revenue for each month to verify
print(f"\nRevenue per Month:")
total_revenue_ytd = 0
for year, month in ytd_months:
    try:
        revenue = totalRevenue(year=year, month=[month], reportId=reportId).Data
        total_revenue_ytd += revenue
        print(f"  {month_names[month]} {year}: ${revenue:,.2f}")
    except Exception as e:
        print(f"  {month_names[month]} {year}: Error - {e}")

print(f"\nTotal YTD Revenue (Sum): ${total_revenue_ytd:,.2f}")

# Also test the direct calculation
print(f"\n" + "=" * 80)
print("Direct YTD Calculation (as per code):")
print("=" * 80)
try:
    ytd_revenue_direct = sum([
        totalRevenue(year=y, month=[m], reportId=reportId).Data
        for y, m in ytd_months
    ])
    print(f"YTD Revenue (Direct): ${ytd_revenue_direct:,.2f}")
    
    # Verify they match
    if abs(ytd_revenue_direct - total_revenue_ytd) < 0.01:
        print("✅ Verification PASSED: Both calculations match!")
    else:
        print(f"❌ Verification FAILED: Mismatch by ${abs(ytd_revenue_direct - total_revenue_ytd):,.2f}")
except Exception as e:
    print(f"❌ Error in direct calculation: {e}")

print("\n" + "=" * 80)
print("Test Case: Financial Year spanning two calendar years")
print("=" * 80)
print(f"\nScenario: Financial Year Start = {financialMonth} (July)")
print(f"Current Month = 1 (January 2026)")
print("\nExpected YTD Months:")
print("  - Jul 2025, Aug 2025, Sep 2025, Oct 2025, Nov 2025, Dec 2025")
print("  - Jan 2026")
print("  Total: 7 months")

# Simulate January 2026
currentYear_sim = 2026
latest_month_sim = 1
ytd_months_sim = []

if latest_month_sim >= financialMonth:
    for m in range(financialMonth, latest_month_sim + 1):
        ytd_months_sim.append((currentYear_sim, m))
else:
    for m in range(financialMonth, 13):
        ytd_months_sim.append((currentYear_sim - 1, m))
    for m in range(1, latest_month_sim + 1):
        ytd_months_sim.append((currentYear_sim, m))

print(f"\nActual YTD Months (from logic):")
for year, month in ytd_months_sim:
    print(f"  - {month_names[month]} {year}")

if len(ytd_months_sim) == 7:
    print("✅ Correct! 7 months calculated for cross-year scenario")
else:
    print(f"❌ Wrong! Expected 7 months, got {len(ytd_months_sim)}")

print("\n")
