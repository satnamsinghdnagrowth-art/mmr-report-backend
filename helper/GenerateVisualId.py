"""
Visual ID Generator for Custom KPIs
Generates unique, collision-free IDs for cards, charts, and tables
"""

import hashlib
import json
import re
from typing import Dict, Any, Optional


def generate_visual_id(
    visual_type: str,
    filtered_data: Dict[str, Any],
    payload_params: Optional[Dict[str, Any]] = None
) -> str:
    """
    Generate unique composite visual ID with parameter hash
    
    Args:
        visual_type: Type of visual ('card', 'chart', or 'table')
        filtered_data: The filtered KPI data containing Report Id and Custom KPIs
        payload_params: Original request parameters (Items, Year, Months, VisualType)
    
    Returns:
        Unique visual ID string (HTML-safe)
    
    Example:
        >>> generate_visual_id('card', {'Report Id': '45373', ...}, {...})
        'custom_kpi_card_45373_wages_and_benefits_pct_a3f9b2e1'
    """
    # Extract basic components
    report_id = str(filtered_data.get('Report Id', 'unknown'))
    custom_kpis = filtered_data.get('Custom KPIs', {})
    first_key = next(iter(custom_kpis.keys()), 'unknown_kpi')
    
    # Sanitize KPI name for HTML ID
    sanitized_kpi = _sanitize_for_html_id(first_key, max_length=50)
    
    # Generate parameter hash for uniqueness
    params_hash = _generate_params_hash(payload_params) if payload_params else 'default'
    
    # Construct final ID
    visual_id = f"custom_kpi_{visual_type}_{report_id}_{sanitized_kpi}_{params_hash}"
    
    return visual_id


def _sanitize_for_html_id(text: str, max_length: int = 50) -> str:
    """
    Sanitize text for use in HTML IDs
    
    Rules:
    - Remove special characters except underscore and hyphen
    - Replace spaces with underscores
    - Convert to lowercase
    - Limit length
    - Ensure starts with letter
    
    Args:
        text: Input text to sanitize
        max_length: Maximum length of output
    
    Returns:
        Sanitized string safe for HTML IDs
    """
    # Replace common patterns
    text = text.replace('%', 'pct')
    text = text.replace('&', 'and')
    text = text.replace('(', '').replace(')', '')
    text = text.replace('[', '').replace(']', '')
    text = text.replace('{', '').replace('}', '')
    
    # Remove special characters, keep alphanumeric, spaces, underscore, hyphen
    text = re.sub(r'[^\w\s-]', '', text)
    
    # Replace whitespace with underscore
    text = re.sub(r'\s+', '_', text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Limit length
    text = text[:max_length]
    
    # Ensure starts with letter
    if text and not text[0].isalpha():
        text = f"kpi_{text}"
    
    # Ensure not empty
    if not text:
        text = "unknown_kpi"
    
    return text


def _generate_params_hash(payload_params: Dict[str, Any]) -> str:
    """
    Generate MD5 hash of request parameters for uniqueness
    
    Args:
        payload_params: Dictionary of request parameters
    
    Returns:
        8-character hash string
    """
    if not payload_params:
        return 'default'
    
    # Extract relevant parameters for hashing
    hash_data = {
        'items': sorted(payload_params.get('Items', [])) if payload_params.get('Items') else [],
        'year': payload_params.get('Year'),
        'months': sorted(payload_params.get('Months', [])) if payload_params.get('Months') else [],
        'visual_type': payload_params.get('VisualType', ''),
    }
    
    # Create deterministic JSON string
    params_str = json.dumps(hash_data, sort_keys=True)
    
    # Generate MD5 hash and take first 8 characters
    hash_obj = hashlib.md5(params_str.encode('utf-8'))
    params_hash = hash_obj.hexdigest()[:8]
    
    return params_hash


def validate_id_components(report_id: Any, kpi_name: str, year: int = None, month: int = None) -> None:
    """
    Validate ID components before generation
    
    Args:
        report_id: Report identifier
        kpi_name: KPI name
        year: Optional year value
        month: Optional month value
    
    Raises:
        ValueError: If any component is invalid
    """
    if not report_id or str(report_id).strip() == "":
        raise ValueError("Report ID is required for visual ID generation")
    
    if not kpi_name or kpi_name.strip() == "":
        raise ValueError("KPI name cannot be empty")
    
    if year is not None and not (1900 <= year <= 2100):
        raise ValueError(f"Invalid year: {year}")
    
    if month is not None and not (1 <= month <= 12):
        raise ValueError(f"Invalid month: {month}")
