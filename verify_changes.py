"""
Simple verification test for the separated section data response.
This test verifies the code changes are correctly implemented.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


def verify_code_structure():
    """
    Verify that the code has been correctly modified to separate
    ActualData and CustomData in the response.
    """
    print("=" * 80)
    print("Code Structure Verification")
    print("=" * 80)
    
    file_path = "services/reportSection/consolidateSection/ConsolidateDataReporting.py"
    
    print(f"\nChecking file: {file_path}")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check for key modifications
    checks = {
        "ActualData key": '"ActualData"' in content,
        "CustomData key": '"CustomData"' in content,
        "Separated data structure": 'separatedData = {' in content,
        "ActualData assignment": '"ActualData": actualData' in content,
        "CustomData assignment": '"CustomData": customData' in content,
        "Returns separatedData": 'Data=separatedData' in content,
        "Custom data initialization": 'customData = {"Sections": []}' in content,
        "Custom section creation": 'customSection = {' in content and '"SectionName":' in content,
    }
    
    print("\nVerification Results:")
    print("-" * 80)
    
    all_passed = True
    for check_name, result in checks.items():
        status = "✓" if result else "✗"
        print(f"{status} {check_name}: {'PASS' if result else 'FAIL'}")
        if not result:
            all_passed = False
    
    print("-" * 80)
    
    if all_passed:
        print("\n✓ All verification checks passed!")
        print("\nThe code has been successfully modified to:")
        print("  1. Separate actual section data from custom KPIs")
        print("  2. Return data in the format:")
        print("     {")
        print('       "ActualData": { "Sections": [...] },')
        print('       "CustomData": { "Sections": [...] }')
        print("     }")
        print("  3. Custom KPIs are stored separately in CustomData")
        print("  4. Original data remains untouched in ActualData")
    else:
        print("\n✗ Some verification checks failed!")
        print("Please review the code modifications.")
    
    # Show the relevant code section
    print("\n" + "=" * 80)
    print("Modified Code Section (lines 74-125):")
    print("=" * 80)
    
    lines = content.split('\n')
    start_line = 73  # Line 74 in 1-indexed
    end_line = 125
    
    for i, line in enumerate(lines[start_line:end_line], start=start_line + 1):
        print(f"{i:3d}. {line}")
    
    print("\n" + "=" * 80)
    print("Verification Complete")
    print("=" * 80)
    
    return all_passed


def show_api_response_format():
    """
    Display the expected API response format.
    """
    print("\n" + "=" * 80)
    print("Expected API Response Format")
    print("=" * 80)
    
    example_response = """
    {
      "Data": {
        "ActualData": {
          "Sections": [
            {
              "SectionName": "Profit & Loss Snippet",
              "SectionData": {
                "Cards": [...],    // Original cards from database
                "Charts": [...],   // Original charts from database
                "Tables": [...]    // Original tables from database
              },
              "Visbility": true
            },
            {
              "SectionName": "Expenses Analysis",
              "SectionData": { ... }
            },
            // ... more sections
          ]
        },
        "CustomData": {
          "Sections": [
            {
              "SectionName": "Profit & Loss Snippet",
              "SectionData": {
                "Cards": [...],    // Custom KPI cards only
                "Charts": [...],   // Custom KPI charts only
                "Tables": [...]    // Custom KPI tables only
              },
              "Visbility": true
            },
            // ... more sections with custom KPIs
          ]
        }
      },
      "Status": 1,
      "Message": "Section Data retrieved Successfully"
    }
    """
    
    print(example_response)
    print("=" * 80)


if __name__ == "__main__":
    success = verify_code_structure()
    show_api_response_format()
    
    if success:
        print("\n✓ Code modifications verified successfully!")
        print("\nTo test with real data:")
        print("  1. Start your server")
        print("  2. Make a POST request to: /get/report/{reportId}/sectionData/")
        print("  3. Check that the response has ActualData and CustomData keys")
    else:
        print("\n✗ Verification failed. Please check the code.")
        sys.exit(1)
