"""
Unit Tests for Visual ID Generation
Tests uniqueness, sanitization, and collision prevention
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helper.GenerateVisualId import (
    generate_visual_id,
    _sanitize_for_html_id,
    _generate_params_hash,
    validate_id_components
)


def test_basic_id_generation():
    """Test basic ID generation"""
    print("Test 1: Basic ID Generation")
    
    filtered_data = {
        'Report Id': '45373',
        'Custom KPIs': {
            'Wages and Benefits (%)': [
                {'Month': 1, 'Year': 2025, 'Value': 4.35}
            ]
        }
    }
    
    payload_params = {
        'Items': ['Wages and Benefits (%)'],
        'Year': 2025,
        'Months': [1],
        'VisualType': 'card'
    }
    
    visual_id = generate_visual_id('card', filtered_data, payload_params)
    
    print(f"  Generated ID: {visual_id}")
    assert visual_id.startswith('custom_kpi_card_45373_')
    assert 'wages_and_benefits_pct' in visual_id
    print("  ✓ PASSED\n")


def test_uniqueness_different_params():
    """Test that different parameters generate different IDs"""
    print("Test 2: Uniqueness with Different Parameters")
    
    filtered_data = {
        'Report Id': '45373',
        'Custom KPIs': {
            'Wages and Benefits (%)': [
                {'Month': 1, 'Year': 2025, 'Value': 4.35}
            ]
        }
    }
    
    params1 = {
        'Items': ['Wages and Benefits (%)'],
        'Year': 2025,
        'Months': [1],
        'VisualType': 'card'
    }
    
    params2 = {
        'Items': ['Wages and Benefits (%)'],
        'Year': 2025,
        'Months': [2],  # Different month
        'VisualType': 'card'
    }
    
    params3 = {
        'Items': ['Wages and Benefits (%)', 'Revenue'],  # Different items
        'Year': 2025,
        'Months': [1],
        'VisualType': 'card'
    }
    
    id1 = generate_visual_id('card', filtered_data, params1)
    id2 = generate_visual_id('card', filtered_data, params2)
    id3 = generate_visual_id('card', filtered_data, params3)
    
    print(f"  ID1 (Month=1):     {id1}")
    print(f"  ID2 (Month=2):     {id2}")
    print(f"  ID3 (Items+1):     {id3}")
    
    assert id1 != id2, "Different months should generate different IDs"
    assert id1 != id3, "Different items should generate different IDs"
    assert id2 != id3, "All three should be unique"
    print("  ✓ PASSED - All IDs are unique\n")


def test_different_visual_types():
    """Test that different visual types generate different IDs"""
    print("Test 3: Different Visual Types")
    
    filtered_data = {
        'Report Id': '45373',
        'Custom KPIs': {
            'Revenue': [{'Month': 1, 'Year': 2025, 'Value': 100}]
        }
    }
    
    params = {
        'Items': ['Revenue'],
        'Year': 2025,
        'Months': [1],
        'VisualType': 'card'
    }
    
    card_id = generate_visual_id('card', filtered_data, params)
    chart_id = generate_visual_id('chart', filtered_data, params)
    table_id = generate_visual_id('table', filtered_data, params)
    
    print(f"  Card ID:  {card_id}")
    print(f"  Chart ID: {chart_id}")
    print(f"  Table ID: {table_id}")
    
    assert 'card' in card_id and 'card' not in chart_id and 'card' not in table_id
    assert 'chart' in chart_id
    assert 'table' in table_id
    assert card_id != chart_id != table_id
    print("  ✓ PASSED\n")


def test_html_id_sanitization():
    """Test HTML ID sanitization"""
    print("Test 4: HTML ID Sanitization")
    
    test_cases = [
        ('Wages and Benefits (%)', 'wages_and_benefits_pct'),
        ('Revenue & Expenses', 'revenue_and_expenses'),
        ('Cost (USD)', 'cost_usd'),
        ('Profit/Loss Ratio', 'profitloss_ratio'),
    ]
    
    for input_text, expected in test_cases:
        result = _sanitize_for_html_id(input_text)
        print(f"  '{input_text}' -> '{result}'")
        assert expected == result, f"Expected '{expected}' but got '{result}'"
    
    # Test that special characters are removed
    result = _sanitize_for_html_id('Test@#$%^&*()Name')
    print(f"  'Test@#$%^&*()Name' -> '{result}'")
    assert 'test' in result and 'name' in result
    
    # Test that it's HTML-safe (no special chars)
    result = _sanitize_for_html_id('A!@#$%^&*()_+B')
    print(f"  'A!@#$%^&*()_+B' -> '{result}'")
    assert result.replace('_', '').replace('pct', '').replace('and', '').isalnum()
    
    print("  ✓ PASSED\n")


def test_same_params_same_id():
    """Test that same parameters generate same ID (deterministic)"""
    print("Test 5: Deterministic ID Generation")
    
    filtered_data = {
        'Report Id': '45373',
        'Custom KPIs': {
            'Revenue': [{'Month': 1, 'Year': 2025, 'Value': 100}]
        }
    }
    
    params = {
        'Items': ['Revenue'],
        'Year': 2025,
        'Months': [1],
        'VisualType': 'card'
    }
    
    id1 = generate_visual_id('card', filtered_data, params)
    id2 = generate_visual_id('card', filtered_data, params)
    
    print(f"  ID1: {id1}")
    print(f"  ID2: {id2}")
    
    assert id1 == id2, "Same parameters should generate same ID"
    print("  ✓ PASSED - IDs are deterministic\n")


def test_empty_and_missing_data():
    """Test handling of empty and missing data"""
    print("Test 6: Empty and Missing Data Handling")
    
    # Empty KPIs
    filtered_data1 = {
        'Report Id': '45373',
        'Custom KPIs': {}
    }
    
    id1 = generate_visual_id('card', filtered_data1, None)
    print(f"  Empty KPIs ID: {id1}")
    assert 'unknown_kpi' in id1
    
    # Missing Report ID
    filtered_data2 = {
        'Custom KPIs': {
            'Revenue': [{'Month': 1, 'Year': 2025, 'Value': 100}]
        }
    }
    
    id2 = generate_visual_id('card', filtered_data2, None)
    print(f"  Missing Report ID: {id2}")
    assert 'unknown' in id2
    
    # No payload
    filtered_data3 = {
        'Report Id': '45373',
        'Custom KPIs': {
            'Revenue': [{'Month': 1, 'Year': 2025, 'Value': 100}]
        }
    }
    
    id3 = generate_visual_id('card', filtered_data3, None)
    print(f"  No payload ID: {id3}")
    assert 'default' in id3
    
    print("  ✓ PASSED\n")


def test_multiple_kpis_same_report():
    """Test that multiple KPIs in same report generate different IDs"""
    print("Test 7: Multiple KPIs in Same Report")
    
    report_id = '45373'
    
    kpi1_data = {
        'Report Id': report_id,
        'Custom KPIs': {
            'Revenue': [{'Month': 1, 'Year': 2025, 'Value': 100}]
        }
    }
    
    kpi2_data = {
        'Report Id': report_id,
        'Custom KPIs': {
            'Expenses': [{'Month': 1, 'Year': 2025, 'Value': 50}]
        }
    }
    
    params = {
        'Items': ['Revenue'],
        'Year': 2025,
        'Months': [1],
        'VisualType': 'card'
    }
    
    id1 = generate_visual_id('card', kpi1_data, params)
    id2 = generate_visual_id('card', kpi2_data, params)
    
    print(f"  Revenue KPI ID:  {id1}")
    print(f"  Expenses KPI ID: {id2}")
    
    assert id1 != id2, "Different KPIs should have different IDs"
    assert 'revenue' in id1
    assert 'expenses' in id2
    print("  ✓ PASSED\n")


def test_hash_consistency():
    """Test hash generation consistency"""
    print("Test 8: Hash Consistency")
    
    params1 = {
        'Items': ['KPI1', 'KPI2'],
        'Year': 2025,
        'Months': [1, 2, 3],
        'VisualType': 'card'
    }
    
    # Same data, different order
    params2 = {
        'Items': ['KPI2', 'KPI1'],  # Different order
        'Months': [3, 1, 2],          # Different order
        'Year': 2025,
        'VisualType': 'card'
    }
    
    hash1 = _generate_params_hash(params1)
    hash2 = _generate_params_hash(params2)
    
    print(f"  Hash1 (original order): {hash1}")
    print(f"  Hash2 (diff order):     {hash2}")
    
    assert hash1 == hash2, "Hash should be same regardless of list order"
    print("  ✓ PASSED - Hashes are order-independent\n")


def test_validation():
    """Test validation function"""
    print("Test 9: Validation")
    
    try:
        validate_id_components("", "KPI Name", 2025, 1)
        assert False, "Should have raised ValueError for empty report ID"
    except ValueError as e:
        print(f"  ✓ Empty report ID validation: {e}")
    
    try:
        validate_id_components("123", "", 2025, 1)
        assert False, "Should have raised ValueError for empty KPI name"
    except ValueError as e:
        print(f"  ✓ Empty KPI name validation: {e}")
    
    try:
        validate_id_components("123", "KPI", 1800, 1)
        assert False, "Should have raised ValueError for invalid year"
    except ValueError as e:
        print(f"  ✓ Invalid year validation: {e}")
    
    try:
        validate_id_components("123", "KPI", 2025, 13)
        assert False, "Should have raised ValueError for invalid month"
    except ValueError as e:
        print(f"  ✓ Invalid month validation: {e}")
    
    print("  ✓ PASSED\n")


def test_long_kpi_names():
    """Test handling of very long KPI names"""
    print("Test 10: Long KPI Names")
    
    long_name = "This is a very long KPI name that exceeds the maximum length limit and should be truncated appropriately"
    
    filtered_data = {
        'Report Id': '45373',
        'Custom KPIs': {
            long_name: [{'Month': 1, 'Year': 2025, 'Value': 100}]
        }
    }
    
    visual_id = generate_visual_id('card', filtered_data, None)
    
    print(f"  Long name: {long_name}")
    print(f"  Generated ID: {visual_id}")
    print(f"  ID length: {len(visual_id)}")
    
    assert len(visual_id) < 150, "ID should be reasonably short"
    print("  ✓ PASSED\n")


def run_all_tests():
    """Run all test cases"""
    print("=" * 60)
    print("CUSTOM KPI VISUAL ID GENERATION - TEST SUITE")
    print("=" * 60)
    print()
    
    try:
        test_basic_id_generation()
        test_uniqueness_different_params()
        test_different_visual_types()
        test_html_id_sanitization()
        test_same_params_same_id()
        test_empty_and_missing_data()
        test_multiple_kpis_same_report()
        test_hash_consistency()
        test_validation()
        test_long_kpi_names()
        
        print("=" * 60)
        print("✓ ALL TESTS PASSED (10/10)")
        print("=" * 60)
        return True
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
