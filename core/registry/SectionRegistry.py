"""
Section Registry - Manages dynamic section IDs
Generates and stores unique IDs for sections when they are created
"""

import json
import os
import uuid
from typing import Optional, Dict
from datetime import datetime

# Configuration
SECTION_REGISTRY_FILE = "database/section_registry.json"


class SectionRegistry:
    """
    Manages section IDs and metadata.
    Generates unique IDs for sections and persists them.
    """
    
    _instance = None
    _registry: Dict[str, Dict] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SectionRegistry, cls).__new__(cls)
            cls._instance._load_registry()
        return cls._instance
    
    def _load_registry(self):
        """Load section registry from file"""
        try:
            if os.path.exists(SECTION_REGISTRY_FILE):
                with open(SECTION_REGISTRY_FILE, 'r', encoding='utf-8') as f:
                    self._registry = json.load(f)
                    print(f"Loaded {len(self._registry)} sections from registry")
            else:
                print("Section registry file not found, initializing empty registry")
                self._registry = {}
                self._initialize_default_sections()
        except Exception as e:
            print(f"Error loading section registry: {e}")
            self._registry = {}
            self._initialize_default_sections()
    
    def _save_registry(self):
        """Save section registry to file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(SECTION_REGISTRY_FILE), exist_ok=True)
            
            with open(SECTION_REGISTRY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self._registry, f, indent=2, ensure_ascii=False)
            print(f"Saved {len(self._registry)} sections to registry")
        except Exception as e:
            print(f"Error saving section registry: {e}")
    
    def _initialize_default_sections(self):
        """Initialize default sections with stable IDs for backwards compatibility"""
        default_sections = {
            "Profit & Loss Snippet": {
                "section_id": "section-001-financial-highlights",
                "section_name": "Profit & Loss Snippet",
                "section_type": "predefined",
                "created_at": datetime.now().isoformat(),
                "description": "Financial highlights and P&L snippet"
            },
            "Expenses Analysis": {
                "section_id": "section-002-expenses-analysis",
                "section_name": "Expenses Analysis",
                "section_type": "predefined",
                "created_at": datetime.now().isoformat(),
                "description": "Detailed expenses analysis"
            },
            "Profitability": {
                "section_id": "section-003-profitability",
                "section_name": "Profitability",
                "section_type": "predefined",
                "created_at": datetime.now().isoformat(),
                "description": "Profitability metrics and analysis"
            },
            "Break-Even Anlaysis": {
                "section_id": "section-004-breakeven-analysis",
                "section_name": "Break-Even Anlaysis",
                "section_type": "predefined",
                "created_at": datetime.now().isoformat(),
                "description": "Break-even analysis"
            },
            "Cash Flow Analysis": {
                "section_id": "section-005-cashflow-analysis",
                "section_name": "Cash Flow Analysis",
                "section_type": "predefined",
                "created_at": datetime.now().isoformat(),
                "description": "Cash flow analysis"
            }
        }
        
        for section_name, metadata in default_sections.items():
            self._registry[section_name] = metadata
        
        self._save_registry()
        print(f"Initialized {len(default_sections)} default sections")
    
    def register_section(
        self,
        section_name: str,
        section_type: str = "custom",
        description: str = "",
        section_id: Optional[str] = None
    ) -> str:
        """
        Register a new section or get existing section ID.
        
        Args:
            section_name: Display name of the section
            section_type: Type of section (predefined, custom)
            description: Optional description
            section_id: Optional specific ID (for migration/backwards compatibility)
        
        Returns:
            section_id: Unique identifier for the section
        """
        # Check if section already exists
        if section_name in self._registry:
            return self._registry[section_name]["section_id"]
        
        # Generate new section ID
        if section_id is None:
            section_id = f"section-{str(uuid.uuid4())[:8]}"
        
        # Store section metadata
        self._registry[section_name] = {
            "section_id": section_id,
            "section_name": section_name,
            "section_type": section_type,
            "created_at": datetime.now().isoformat(),
            "description": description,
            "updated_at": datetime.now().isoformat()
        }
        
        self._save_registry()
        print(f"Registered new section: {section_name} -> {section_id}")
        
        return section_id
    
    def get_section_id(self, section_name: str) -> Optional[str]:
        """
        Get section ID by section name.
        If section doesn't exist, register it automatically.
        
        Args:
            section_name: Display name of the section
        
        Returns:
            section_id or None if not found
        """
        if section_name in self._registry:
            return self._registry[section_name]["section_id"]
        
        # Auto-register unknown sections as custom
        print(f"Auto-registering unknown section: {section_name}")
        return self.register_section(section_name, section_type="custom")
    
    def get_section_name(self, section_id: str) -> Optional[str]:
        """
        Get section name by section ID.
        
        Args:
            section_id: Unique identifier
        
        Returns:
            section_name or None if not found
        """
        for name, metadata in self._registry.items():
            if metadata["section_id"] == section_id:
                return name
        return None
    
    def get_section_metadata(self, section_name: str) -> Optional[Dict]:
        """
        Get full metadata for a section.
        
        Args:
            section_name: Display name of the section
        
        Returns:
            metadata dictionary or None
        """
        return self._registry.get(section_name)
    
    def update_section_name(self, old_name: str, new_name: str) -> bool:
        """
        Update section display name while keeping the same ID.
        
        Args:
            old_name: Current section name
            new_name: New section name
        
        Returns:
            True if successful, False otherwise
        """
        if old_name not in self._registry:
            print(f"Section not found: {old_name}")
            return False
        
        # Get the metadata
        metadata = self._registry[old_name]
        metadata["section_name"] = new_name
        metadata["updated_at"] = datetime.now().isoformat()
        
        # Move to new key
        self._registry[new_name] = metadata
        del self._registry[old_name]
        
        self._save_registry()
        print(f"Updated section name: {old_name} -> {new_name}")
        
        return True
    
    def list_all_sections(self) -> Dict[str, Dict]:
        """Get all registered sections"""
        return self._registry.copy()
    
    def delete_section(self, section_name: str) -> bool:
        """
        Delete a section from registry (only for custom sections).
        
        Args:
            section_name: Display name of the section
        
        Returns:
            True if successful, False otherwise
        """
        if section_name not in self._registry:
            return False
        
        # Prevent deletion of predefined sections
        if self._registry[section_name].get("section_type") == "predefined":
            print(f"Cannot delete predefined section: {section_name}")
            return False
        
        del self._registry[section_name]
        self._save_registry()
        print(f"Deleted section: {section_name}")
        
        return True


# Singleton instance
_section_registry = None


def get_section_registry() -> SectionRegistry:
    """Get the singleton section registry instance"""
    global _section_registry
    if _section_registry is None:
        _section_registry = SectionRegistry()
    return _section_registry


# Convenience functions
def get_section_id(section_name: str) -> str:
    """Get or create section ID for a section name"""
    return get_section_registry().get_section_id(section_name)


def get_section_name(section_id: str) -> Optional[str]:
    """Get section name from section ID"""
    return get_section_registry().get_section_name(section_id)


def register_section(section_name: str, section_type: str = "custom", description: str = "") -> str:
    """Register a new section and get its ID"""
    return get_section_registry().register_section(section_name, section_type, description)


def update_section_name(old_name: str, new_name: str) -> bool:
    """Update section display name"""
    return get_section_registry().update_section_name(old_name, new_name)


def list_all_sections() -> Dict[str, Dict]:
    """List all registered sections"""
    return get_section_registry().list_all_sections()
