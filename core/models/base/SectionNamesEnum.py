from enum import Enum


class SectionName(Enum):
    FinancialHighlights = "Profit & Loss Snippet"
    ExpensesAnalysis = "Expenses Analysis"
    Profitability = "Profitability"
    BreakevenAnlaysis = "Break-Even Anlaysis"
    CashFlowAnalysis = "Cash Flow Analysis"


# Import registry functions for dynamic section ID management
from core.registry.SectionRegistry import (
    get_section_id as _get_section_id,
    get_section_name as _get_section_name,
    register_section as _register_section,
    update_section_name as _update_section_name,
    list_all_sections as _list_all_sections
)


# Helper function to get section ID from name
def get_section_id(section_name: str) -> str:
    """
    Get section ID from section name.
    Automatically registers unknown sections.
    """
    return _get_section_id(section_name)


# Helper function to get section name from ID
def get_section_name(section_id: str) -> str:
    """Get section name from section ID"""
    return _get_section_name(section_id)


# Helper function to register new section
def register_section(section_name: str, section_type: str = "custom", description: str = "") -> str:
    """Register a new section and get its ID"""
    return _register_section(section_name, section_type, description)


# Helper function to update section name
def update_section_name(old_name: str, new_name: str) -> bool:
    """Update section display name while keeping the same ID"""
    return _update_section_name(old_name, new_name)


# Helper function to list all sections
def list_all_sections():
    """List all registered sections with metadata"""
    return _list_all_sections()
