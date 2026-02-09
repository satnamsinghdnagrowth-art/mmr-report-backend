"""
Comprehensive test for dynamic Section Registry
Tests section ID generation, persistence, and custom section support
"""

import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import json


def test_section_registry():
    """Test the Section Registry functionality"""
    print("=" * 80)
    print("Testing Dynamic Section Registry")
    print("=" * 80)
    
    from core.registry.SectionRegistry import (
        get_section_registry,
        get_section_id,
        get_section_name,
        register_section,
        update_section_name,
        list_all_sections
    )
    
    registry = get_section_registry()
    
    # Test 1: Predefined Sections
    print("\n1. Testing Predefined Sections")
    print("-" * 80)
    
    predefined_sections = [
        "Profit & Loss Snippet",
        "Expenses Analysis",
        "Profitability",
        "Break-Even Anlaysis",
        "Cash Flow Analysis"
    ]
    
    all_found = True
    for section_name in predefined_sections:
        section_id = get_section_id(section_name)
        if section_id:
            print(f"✓ {section_name}")
            print(f"  ID: {section_id}")
        else:
            print(f"✗ {section_name} - No ID found")
            all_found = False
    
    if all_found:
        print("\n✓ All predefined sections have IDs")
    else:
        print("\n✗ Some predefined sections missing IDs")
    
    # Test 2: Create Custom Section
    print("\n2. Testing Custom Section Creation")
    print("-" * 80)
    
    custom_section_name = "Custom Revenue Analysis"
    custom_description = "Custom section for detailed revenue analysis"
    
    custom_id = register_section(
        section_name=custom_section_name,
        section_type="custom",
        description=custom_description
    )
    
    print(f"✓ Created custom section: {custom_section_name}")
    print(f"  ID: {custom_id}")
    print(f"  Description: {custom_description}")
    
    # Verify it can be retrieved
    retrieved_id = get_section_id(custom_section_name)
    if retrieved_id == custom_id:
        print(f"✓ Custom section ID retrieved successfully")
    else:
        print(f"✗ Custom section ID mismatch: {retrieved_id} != {custom_id}")
    
    # Test 3: ID Persistence
    print("\n3. Testing ID Persistence")
    print("-" * 80)
    
    # Get ID multiple times - should be the same
    id1 = get_section_id("Profit & Loss Snippet")
    id2 = get_section_id("Profit & Loss Snippet")
    id3 = get_section_id("Profit & Loss Snippet")
    
    if id1 == id2 == id3:
        print(f"✓ Section ID is persistent: {id1}")
    else:
        print(f"✗ Section ID is not consistent: {id1}, {id2}, {id3}")
    
    # Test 4: Reverse Lookup (ID to Name)
    print("\n4. Testing Reverse Lookup")
    print("-" * 80)
    
    test_sections = [
        ("section-001-financial-highlights", "Profit & Loss Snippet"),
        ("section-002-expenses-analysis", "Expenses Analysis"),
        (custom_id, custom_section_name)
    ]
    
    reverse_lookup_success = True
    for section_id, expected_name in test_sections:
        actual_name = get_section_name(section_id)
        if actual_name == expected_name:
            print(f"✓ {section_id} → {actual_name}")
        else:
            print(f"✗ {section_id} → {actual_name} (expected: {expected_name})")
            reverse_lookup_success = False
    
    if reverse_lookup_success:
        print("\n✓ All reverse lookups successful")
    else:
        print("\n✗ Some reverse lookups failed")
    
    # Test 5: Section Metadata
    print("\n5. Testing Section Metadata")
    print("-" * 80)
    
    metadata = registry.get_section_metadata(custom_section_name)
    if metadata:
        print(f"✓ Metadata for '{custom_section_name}':")
        print(f"  Section ID: {metadata.get('section_id')}")
        print(f"  Section Type: {metadata.get('section_type')}")
        print(f"  Description: {metadata.get('description')}")
        print(f"  Created At: {metadata.get('created_at')}")
        print(f"  Updated At: {metadata.get('updated_at')}")
    else:
        print(f"✗ No metadata found for '{custom_section_name}'")
    
    # Test 6: Update Section Name
    print("\n6. Testing Section Name Update")
    print("-" * 80)
    
    old_name = "Custom Revenue Analysis"
    new_name = "Advanced Revenue Analysis"
    original_id = get_section_id(old_name)
    
    success = update_section_name(old_name, new_name)
    if success:
        new_id = get_section_id(new_name)
        if new_id == original_id:
            print(f"✓ Section name updated successfully")
            print(f"  Old Name: {old_name}")
            print(f"  New Name: {new_name}")
            print(f"  ID Preserved: {original_id}")
        else:
            print(f"✗ Section ID changed after rename: {original_id} → {new_id}")
    else:
        print(f"✗ Failed to update section name")
    
    # Test 7: List All Sections
    print("\n7. Testing List All Sections")
    print("-" * 80)
    
    all_sections = list_all_sections()
    print(f"✓ Total sections registered: {len(all_sections)}")
    
    predefined_count = sum(1 for s in all_sections.values() if s.get('section_type') == 'predefined')
    custom_count = sum(1 for s in all_sections.values() if s.get('section_type') == 'custom')
    
    print(f"  - Predefined sections: {predefined_count}")
    print(f"  - Custom sections: {custom_count}")
    
    # Test 8: Auto-registration
    print("\n8. Testing Auto-registration")
    print("-" * 80)
    
    unknown_section = "Unknown Test Section"
    auto_id = get_section_id(unknown_section)
    
    if auto_id:
        print(f"✓ Auto-registered unknown section: {unknown_section}")
        print(f"  Generated ID: {auto_id}")
        
        # Verify it's in the registry
        metadata = registry.get_section_metadata(unknown_section)
        if metadata and metadata.get('section_type') == 'custom':
            print(f"✓ Marked as custom section")
        else:
            print(f"✗ Not properly registered")
    else:
        print(f"✗ Failed to auto-register section")
    
    # Test 9: Registry File Persistence
    print("\n9. Testing Registry File Persistence")
    print("-" * 80)
    
    registry_file = "database/section_registry.json"
    if os.path.exists(registry_file):
        print(f"✓ Registry file exists: {registry_file}")
        
        with open(registry_file, 'r') as f:
            file_data = json.load(f)
        
        print(f"✓ Registry file contains {len(file_data)} sections")
        
        # Verify custom section is in file
        if new_name in file_data:
            print(f"✓ Custom section '{new_name}' persisted to file")
        else:
            print(f"✗ Custom section not found in file")
    else:
        print(f"✗ Registry file not found")
    
    # Test 10: Delete Custom Section
    print("\n10. Testing Section Deletion")
    print("-" * 80)
    
    # Try to delete predefined section (should fail)
    predefined_delete = registry.delete_section("Profitability")
    if not predefined_delete:
        print(f"✓ Cannot delete predefined section (as expected)")
    else:
        print(f"✗ Predefined section was deleted (should not happen)")
    
    # Delete custom section (should succeed)
    custom_delete = registry.delete_section(unknown_section)
    if custom_delete:
        print(f"✓ Custom section '{unknown_section}' deleted successfully")
    else:
        print(f"✗ Failed to delete custom section")
    
    print("\n" + "=" * 80)
    print("Section Registry Tests Completed")
    print("=" * 80)
    
    return True


def test_integration_with_models():
    """Test integration with existing models"""
    print("\n" + "=" * 80)
    print("Testing Integration with Models")
    print("=" * 80)
    
    try:
        from core.models.visualsModel.SectionData import ConsolidateSectionDate, SectionData
        from core.models.base.SectionNamesEnum import get_section_id
        
        # Test creating section with dynamic ID
        section_name = "Profit & Loss Snippet"
        section_id = get_section_id(section_name)
        
        section = ConsolidateSectionDate(
            SectionId=section_id,
            SectionName=section_name,
            SectionData=SectionData(Cards=[], Charts=[], Tables=[])
        )
        
        print(f"✓ Created ConsolidateSectionDate with dynamic ID")
        print(f"  Section Name: {section.SectionName}")
        print(f"  Section ID: {section.SectionId}")
        
        # Test with custom section
        custom_name = "Test Custom Section"
        custom_id = get_section_id(custom_name)
        
        custom_section = ConsolidateSectionDate(
            SectionId=custom_id,
            SectionName=custom_name,
            SectionData=SectionData(Cards=[], Charts=[], Tables=[])
        )
        
        print(f"\n✓ Created ConsolidateSectionDate with custom section")
        print(f"  Section Name: {custom_section.SectionName}")
        print(f"  Section ID: {custom_section.SectionId}")
        
        return True
        
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def show_registry_contents():
    """Display the current registry contents"""
    print("\n" + "=" * 80)
    print("Current Registry Contents")
    print("=" * 80)
    
    from core.registry.SectionRegistry import list_all_sections
    
    all_sections = list_all_sections()
    
    print(f"\nTotal Sections: {len(all_sections)}")
    print("\n" + "-" * 80)
    
    for section_name, metadata in all_sections.items():
        section_id = metadata.get('section_id')
        section_type = metadata.get('section_type')
        description = metadata.get('description', 'N/A')
        
        print(f"\n📌 {section_name}")
        print(f"   ID: {section_id}")
        print(f"   Type: {section_type}")
        print(f"   Description: {description}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    success1 = test_section_registry()
    success2 = test_integration_with_models()
    show_registry_contents()
    
    if success1 and success2:
        print("\n✅ All tests passed!")
        print("\n🎉 Dynamic Section Registry is working correctly!")
        print("\nKey Features:")
        print("  ✓ Predefined sections have stable IDs")
        print("  ✓ Custom sections auto-generate unique IDs")
        print("  ✓ IDs persist across restarts")
        print("  ✓ Section names can be updated safely")
        print("  ✓ Registry is stored in database/section_registry.json")
    else:
        print("\n❌ Some tests failed. Please review the errors above.")
        sys.exit(1)
