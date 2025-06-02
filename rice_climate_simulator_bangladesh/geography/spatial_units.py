from typing import List, Optional, Dict
from enum import Enum

class SpatialScale(Enum):
    NATIONAL = "National"
    DIVISION = "Division"
    DISTRICT = "District"
    UPAZILA = "Upazila"
    VILLAGE = "Village"
    AEZ = "AgroEcologicalZone"

class AdministrativeUnit:
    """Represents a generic administrative unit."""
    def __init__(self, unit_id: str, name: str, scale: SpatialScale, parent_id: Optional[str] = None):
        self.unit_id = unit_id
        self.name = name
        self.scale = scale
        self.parent_id = parent_id  # ID of the parent unit (e.g., District's parent is Division)
        self.children_ids: List[str] = [] # IDs of child units (e.g., Division's children are Districts)
        self.attributes: Dict[str, any] = {} # For additional data like population, area, etc.

    def __repr__(self):
        return f"{self.scale.value}(id='{self.unit_id}', name='{self.name}')"

class AgroEcologicalZone:
    """Represents an Agro-Ecological Zone (AEZ)."""
    def __init__(self, aez_id: str, name: str, description: Optional[str] = None):
        self.aez_id = aez_id
        self.name = name
        self.description = description
        self.characteristics: Dict[str, any] = {} # e.g., soil_type, rainfall_pattern

    def __repr__(self):
        return f"AEZ(id='{self.aez_id}', name='{self.name}')"

# Example Usage (will be populated by data loader)
# divisions = [
#     AdministrativeUnit(unit_id="div1", name="Barishal", scale=SpatialScale.DIVISION),
#     # ... other divisions
# ]
# aezs = [
#     AgroEcologicalZone(aez_id="aez1", name="Zone 1", description="Highland area"),
#     # ... other AEZs
# ]
