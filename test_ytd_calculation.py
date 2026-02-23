#!/usr/bin/env python3
"""
Test script to verify YTD calculation based on Financial Year Start
"""
import requests
import json

# API endpoint
API_URL = "http://192.168.29.85:8081/api/v1/section/financialHighlights/get/report/75222/sectionData/"

# Request payload
payload = {
    "Year": 2025,
    "Months": [10],  # October 2025
    "ReportType": "Month",
    "SectionName": "Financial Heights"
}

print("=" * 80)
print("Testing YTD Calculation with Financial Year Start")
print("=" * 80)
print(f"\nRequest Payload:")
print(json.dumps(payload, indent=2))
print(f"\nSending POST request to: {API_URL}")

try:
    response = requests.post(API_URL, json=payload, timeout=30)
    
    print(f"\nResponse Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        # Find INCOME_STATEMENT_TABLE
        if "Data" in data and "Tables" in data["Data"]:
            tables = data["Data"]["Tables"]
            income_statement = None
            
            for table in tables:
                if table.get("Id") == "INCOME_STATEMENT_TABLE":
                    income_statement = table
                    break
            
            if income_statement:
                print("\n" + "=" * 80)
                print("INCOME_STATEMENT_TABLE Found!")
                print("=" * 80)
                print(f"\nTitle: {income_statement.get('Title')}")
                print(f"\nColumns: {income_statement.get('Column')}")
                
                # Check YTD column (should be the last column)
                columns = income_statement.get('Column', [])
                if len(columns) > 0:
                    ytd_column = columns[-1]
                    print(f"\nYTD Column Name: {ytd_column}")
                
                # Print first few rows to verify YTD values
                print("\n" + "-" * 80)
                print("Sample Rows (First 3):")
                print("-" * 80)
                
                rows = income_statement.get('Rows', [])
                for i, row in enumerate(rows[:3]):
                    if len(row) > 0:
                        particular = row[0].get('Value', 'N/A')
                        ytd_value = row[-1].get('Value', 'N/A') if len(row) > 5 else 'N/A'
                        print(f"{i+1}. {particular}: YTD = {ytd_value}")
                
                print("\n" + "=" * 80)
                print("Test completed successfully!")
                print("=" * 80)
                
                # Additional verification
                print("\n📊 Verification Notes:")
                print("- Financial Year Start: Check Report Details for 'Financial Year' value")
                print("- YTD should calculate from Financial Year start month to current month")
                print("- If Financial Year = 7 (July) and Current Month = 1 (Jan), YTD should include:")
                print("  July, Aug, Sep, Oct, Nov, Dec (2025) + Jan (2026) = 7 months")
                
            else:
                print("\n❌ INCOME_STATEMENT_TABLE not found in response")
                print("\nAvailable tables:")
                for table in tables:
                    print(f"  - {table.get('Id')}")
        else:
            print("\n❌ Response structure unexpected")
            print(json.dumps(data, indent=2)[:500])
    else:
        print(f"\n❌ Error: {response.text}")

except requests.exceptions.RequestException as e:
    print(f"\n❌ Request failed: {e}")
except Exception as e:
    print(f"\n❌ Unexpected error: {e}")

print("\n")
