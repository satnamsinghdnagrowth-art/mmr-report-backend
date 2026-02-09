# Dynamic Section ID System - Implementation Guide

## Overview

Implemented a dynamic section ID system that generates and persists unique IDs for sections when they are created. This approach supports both predefined sections and future custom sections, making the system highly scalable and maintainable.

## Why Dynamic IDs?

**Problem with Hardcoded IDs:**
- Static enum values don't scale with custom sections
- Adding new sections requires code changes
- No flexibility for user-defined sections

**Solution - Dynamic Registry:**
- IDs generated automatically when sections are created
- Persistent storage in JSON file
- Supports unlimited custom sections
- Zero code changes needed for new sections

## Architecture

### Components

1. **SectionRegistry** (`core/registry/SectionRegistry.py`)
   - Singleton class managing all section IDs
   - Generates unique IDs using UUID
   - Persists to `database/section_registry.json`
   - Provides CRUD operations for sections

2. **Helper Functions** (`core/models/base/SectionNamesEnum.py`)
   - Wrapper functions for easy access
   - Backwards compatible interface
   - Integration with existing code

3. **Registry File** (`database/section_registry.json`)
   - JSON file storing section metadata
   - Auto-created on first use
   - Includes timestamps, types, descriptions

### Section ID Format

**Predefined Sections (Stable IDs):**
```
section-001-financial-highlights
section-002-expenses-analysis
section-003-profitability
section-004-breakeven-analysis
section-005-cashflow-analysis
```

**Custom Sections (UUID-based):**
```
section-{uuid}
Example: section-5c09fd8d, section-98a56157
```

## Usage Guide

### Getting Section ID

```python
from core.models.base.SectionNamesEnum import get_section_id

# For predefined section
section_id = get_section_id("Profit & Loss Snippet")
# Returns: "section-001-financial-highlights"

# For custom section (auto-registers if new)
section_id = get_section_id("My Custom Section")
# Returns: "section-{uuid}" (e.g., "section-a1b2c3d4")
```

### Registering New Section

```python
from core.models.base.SectionNamesEnum import register_section

# Register with metadata
section_id = register_section(
    section_name="Revenue Forecast",
    section_type="custom",
    description="Monthly revenue forecasting section"
)

print(f"New section ID: {section_id}")
```

### Getting Section Name from ID

```python
from core.models.base.SectionNamesEnum import get_section_name

section_name = get_section_name("section-001-financial-highlights")
# Returns: "Profit & Loss Snippet"
```

### Updating Section Name

```python
from core.models.base.SectionNamesEnum import update_section_name

# Rename section while keeping same ID
success = update_section_name(
    old_name="Revenue Forecast",
    new_name="Advanced Revenue Forecast"
)

# ID remains the same, only display name changes
```

### Listing All Sections

```python
from core.models.base.SectionNamesEnum import list_all_sections

all_sections = list_all_sections()
for name, metadata in all_sections.items():
    print(f"{name}: {metadata['section_id']}")
```

## API Integration

### Creating Sections

```python
from core.models.visualsModel.SectionData import ConsolidateSectionDate, SectionData
from core.models.base.SectionNamesEnum import get_section_id

# Create section with auto-generated ID
section = ConsolidateSectionDate(
    SectionId=get_section_id("Profit & Loss Snippet"),
    SectionName="Profit & Loss Snippet",
    SectionData=SectionData(Cards=[], Charts=[], Tables=[])
)
```

### Custom KPI with Section ID

```python
from core.models.visualsModel.CustomKpiModel import CustomKpiRequestModel
from core.models.base.SectionNamesEnum import get_section_id

# Section ID auto-populated from name
custom_kpi = CustomKpiRequestModel(
    VisualType="Card",
    Items=["Revenue", "Expenses"],
    SectionName="Custom Revenue Analysis",
    SectionId=get_section_id("Custom Revenue Analysis")  # Auto-generates if new
)
```

## Registry File Structure

**Location:** `database/section_registry.json`

```json
{
  "Profit & Loss Snippet": {
    "section_id": "section-001-financial-highlights",
    "section_name": "Profit & Loss Snippet",
    "section_type": "predefined",
    "created_at": "2026-02-06T15:04:31.791618",
    "description": "Financial highlights and P&L snippet"
  },
  "Custom Revenue Analysis": {
    "section_id": "section-5c09fd8d",
    "section_name": "Custom Revenue Analysis",
    "section_type": "custom",
    "created_at": "2026-02-06T15:04:31.791824",
    "description": "Custom section for detailed revenue analysis",
    "updated_at": "2026-02-06T15:04:31.792032"
  }
}
```

### Metadata Fields

- **section_id**: Unique identifier (stable, never changes)
- **section_name**: Display name (can be updated)
- **section_type**: `predefined` or `custom`
- **created_at**: ISO timestamp of creation
- **updated_at**: ISO timestamp of last update
- **description**: Optional description

## Key Features

### 1. Auto-Registration
Unknown sections are automatically registered when first accessed:

```python
# First time accessing unknown section
section_id = get_section_id("New Custom Section")
# Automatically creates entry with generated ID
```

### 2. ID Stability
Section IDs never change, even when names are updated:

```python
old_id = get_section_id("Revenue Analysis")
update_section_name("Revenue Analysis", "Advanced Revenue Analysis")
new_id = get_section_id("Advanced Revenue Analysis")
assert old_id == new_id  # True - ID preserved
```

### 3. Persistence
Registry automatically saves to file on every change:

```python
register_section("Test Section")
# Immediately persisted to database/section_registry.json
```

### 4. Singleton Pattern
Single registry instance shared across application:

```python
from core.registry.SectionRegistry import get_section_registry

registry = get_section_registry()  # Always same instance
```

### 5. Type Safety
Distinguish between predefined and custom sections:

```python
sections = list_all_sections()
for name, meta in sections.items():
    if meta['section_type'] == 'predefined':
        print(f"Built-in: {name}")
    else:
        print(f"Custom: {name}")
```

## Benefits Over Static Enums

| Feature | Static Enum | Dynamic Registry |
|---------|-------------|------------------|
| Add custom sections | ❌ Requires code change | ✅ Automatic |
| Scalability | ❌ Limited | ✅ Unlimited |
| User-defined sections | ❌ Not possible | ✅ Fully supported |
| ID persistence | ✅ Yes | ✅ Yes |
| Rename safety | ✅ Yes | ✅ Yes |
| Metadata storage | ❌ No | ✅ Yes (timestamps, descriptions) |
| Database backup | ❌ N/A | ✅ Simple JSON file |

## Testing

### Run Tests

```bash
python test_section_ids.py
```

### Test Coverage

✅ Predefined section ID retrieval  
✅ Custom section creation  
✅ ID persistence across calls  
✅ Reverse lookup (ID → name)  
✅ Section metadata retrieval  
✅ Section name updates  
✅ List all sections  
✅ Auto-registration  
✅ File persistence  
✅ Section deletion (custom only)  
✅ Integration with models

## Migration from Static IDs

The system is fully backwards compatible:

**Before (Static):**
```python
from core.models.base.SectionNamesEnum import SectionId

section_id = SectionId.FinancialHighlights.value
```

**After (Dynamic):**
```python
from core.models.base.SectionNamesEnum import get_section_id

section_id = get_section_id("Profit & Loss Snippet")
```

**Result:** Same IDs, more flexibility!

## Best Practices

### 1. Always Use Helper Functions
```python
# ✅ Good
from core.models.base.SectionNamesEnum import get_section_id
section_id = get_section_id(section_name)

# ❌ Avoid
from core.registry.SectionRegistry import SectionRegistry
registry = SectionRegistry()
section_id = registry.get_section_id(section_name)
```

### 2. Let Auto-Registration Work
```python
# ✅ Good - Auto-registers if needed
section_id = get_section_id("New Section")

# ❌ Unnecessary
if section_name not in registry:
    register_section(section_name)
section_id = get_section_id(section_name)
```

### 3. Provide Descriptions for Custom Sections
```python
# ✅ Good
register_section(
    "Revenue Forecast",
    section_type="custom",
    description="Monthly revenue forecasting and analysis"
)

# ⚠️ Works but less informative
register_section("Revenue Forecast")
```

### 4. Use Section IDs in Queries
```python
# ✅ Good - Stable reference
for section in sections:
    if section['SectionId'] == get_section_id("Profitability"):
        # Process section

# ⚠️ Works but fragile
for section in sections:
    if section['SectionName'] == "Profitability":
        # Breaks if name changes
```

## Troubleshooting

### Registry File Missing
**Symptom:** "Section registry file not found"  
**Solution:** Normal on first run. Registry auto-initializes with predefined sections.

### Section Not Found
**Symptom:** `get_section_name()` returns `None`  
**Solution:** Section ID doesn't exist. Check the ID or use `list_all_sections()` to see available sections.

### Cannot Delete Section
**Symptom:** "Cannot delete predefined section"  
**Solution:** Predefined sections cannot be deleted. Only custom sections can be removed.

### Registry File Corrupted
**Symptom:** JSON decode error  
**Solution:** Delete `database/section_registry.json` and restart. Registry will reinitialize.

## Files Created/Modified

### New Files
- ✅ `core/registry/SectionRegistry.py` - Dynamic registry implementation
- ✅ `database/section_registry.json` - Persistent storage (auto-created)
- ✅ `test_section_ids.py` - Comprehensive test suite

### Modified Files
- ✏️ `core/models/base/SectionNamesEnum.py` - Updated to use registry
- ✏️ `services/reportSection/consolidateSection/ConsolidateDataReporting.py` - Uses registry
- ✏️ `services/customKPIs/CreateCustomKPIsList.py` - Uses registry

## Summary

✅ **Dynamic ID Generation** - UUIDs for custom sections  
✅ **Persistent Storage** - JSON file in database/  
✅ **Auto-Registration** - Unknown sections registered automatically  
✅ **Backwards Compatible** - Predefined sections keep stable IDs  
✅ **Scalable** - Supports unlimited custom sections  
✅ **Type Safe** - Distinguish predefined vs custom  
✅ **Metadata Rich** - Timestamps, descriptions, types  
✅ **Well Tested** - Comprehensive test suite included

The system is production-ready and supports future growth with custom user-defined sections!
