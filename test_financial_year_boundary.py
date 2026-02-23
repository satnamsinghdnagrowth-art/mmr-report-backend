#!/usr/bin/env python3
"""
Comprehensive test to verify YTD calculation does NOT include previous year
when financial year starts in current year.

Test Case: Financial Year = January, Current Month = January 2026
Expected: YTD should ONLY include January 2026, NOT 2025 months
"""
import requests
import json

print("=" * 80)
print("TEST: Financial Year Boundary Verification")
print("=" * 80)
print()
print("📋 Test Scenario:")
print("  - Company: Hey Bagel, LLC")
print("  - Report ID: 30712")
print("  - Financial Year Start: January (Month 1)")
print("  - Current Month: January 2026")
print("  - Data Available: Aug-Dec 2025, Jan 2026")
print()
print("❓ Question: Should YTD include Aug-Dec 2025?")
print("✅ Answer: NO - Financial year starts in Jan 2026, so YTD = Jan 2026 only")
print()

# API request
API_URL = "http://192.168.29.85:8081/api/v1/section/financialHighlights/get/report/30712/sectionData/"
payload = {
    "Year": 2026,
    "Months": [1],
    "ReportType": "Month",
    "SectionName": "Financial Heights"
}

print("=" * 80)
print("Making API Request...")
print("=" * 80)

try:
    response = requests.post(API_URL, json=payload, timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        
        # Find INCOME_STATEMENT_TABLE
        tables = data.get("Data", {}).get("Tables", [])
        income_statement = None
        
        for table in tables:
            if table.get("Id") == "INCOME_STATEMENT_TABLE":
                income_statement = table
                break
        
        if income_statement:
            print()
            print("✅ INCOME_STATEMENT_TABLE Retrieved")
            print()
            
            columns = income_statement.get('Column', [])
            rows = income_statement.get('Rows', [])
            
            # Print header
            print("Columns:", columns)
            print()
            
            # Analyze Revenue row
            if len(rows) > 0:
                revenue_row = rows[0]
                particular = revenue_row[0].get('Value')
                jan_2026 = revenue_row[1].get('Value')
                dec_2025 = revenue_row[2].get('Value')
                ytd_2026 = revenue_row[-1].get('Value')
                
                print("=" * 80)
                print("REVENUE ANALYSIS")
                print("=" * 80)
                print(f"  Jan 2026:  ${jan_2026:,.2f}")
                print(f"  Dec 2025:  ${dec_2025:,.2f}")
                print(f"  YTD 2026:  ${ytd_2026:,.2f}")
                print()
                
                # Verification
                print("=" * 80)
                print("VERIFICATION")
                print("=" * 80)
                
                if abs(ytd_2026 - jan_2026) < 0.01:
                    print("✅ PASS: YTD equals Jan 2026 only")
                    print("   - YTD does NOT include 2025 months")
                    print("   - Financial year boundary is respected")
                    print("   - Implementation is CORRECT")
                else:
                    print("❌ FAIL: YTD does not match Jan 2026")
                    print(f"   Expected: ${jan_2026:,.2f}")
                    print(f"   Got: ${ytd_2026:,.2f}")
                    print(f"   Difference: ${abs(ytd_2026 - jan_2026):,.2f}")
                
                print()
                
                # Additional check
                if ytd_2026 > jan_2026 + 1000:
                    print("⚠️  WARNING: YTD is significantly larger than Jan 2026")
                    print("   This suggests it might be including previous months")
                    print(f"   Possible months: Aug-Dec 2025 + Jan 2026")
                
                print()
                print("=" * 80)
                print("CONCLUSION")
                print("=" * 80)
                print()
                if abs(ytd_2026 - jan_2026) < 0.01:
                    print("🎉 TEST PASSED!")
                    print()
                    print("The YTD calculation correctly:")
                    print("  1. Respects the financial year start (January)")
                    print("  2. Only includes months from the current financial year")
                    print("  3. Does NOT include previous year months (Aug-Dec 2025)")
                    print("  4. YTD for Jan 2026 = Jan 2026 only")
                else:
                    print("❌ TEST FAILED - Implementation needs fixing")
                
                # Show all rows for complete picture
                print()
                print("=" * 80)
                print("COMPLETE TABLE DATA")
                print("=" * 80)
                print()
                for i, row in enumerate(rows[:5]):
                    if len(row) > 5:
                        label = row[0].get('Value')
                        current = row[1].get('Value')
                        ytd = row[-1].get('Value')
                        print(f"{i+1}. {label:30s} Current: ${current:>12,.2f}  YTD: ${ytd:>12,.2f}")
        else:
            print("❌ INCOME_STATEMENT_TABLE not found")
    else:
        print(f"❌ API Error: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"❌ Error: {e}")

print()
