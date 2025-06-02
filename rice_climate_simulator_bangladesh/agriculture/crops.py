from enum import Enum
from typing import Optional, Dict, List

class RiceSeason(Enum):
    AUS = "Aus (March-June, Pre-Monsoon)"
    AMAN = "Aman (July-November, Monsoon)"
    BORO = "Boro (December-May, Dry Season Irrigated)"

class AmanSubVariety(Enum):
    BROADCAST_AMAN = "Broadcast Aman (B. Aman)"
    TRANSPLANTED_AMAN = "Transplanted Aman (T. Aman)"

class RiceVariety:
    """Represents a specific rice variety with its characteristics."""
    def __init__(self, variety_id: str, name: str, season: RiceSeason,
                 is_hyv: bool = False, # High Yielding Variety
                 is_salt_tolerant: bool = False,
                 is_drought_tolerant: bool = False,
                 is_flood_tolerant: bool = False,
                 maturity_days: int = 120, # Average days to maturity
                 potential_yield_t_ha: float = 5.0, # Potential yield in tons per hectare under optimal conditions
                 water_requirement_mm: int = 1200, # Total water requirement in mm
                 input_costs_bdt_ha: float = 20000, # Placeholder for input costs (seeds, fertilizer, etc.)
                 attributes: Optional[Dict[str, any]] = None
                 ):
        self.variety_id = variety_id
        self.name = name
        self.season = season
        self.is_hyv = is_hyv
        self.is_salt_tolerant = is_salt_tolerant
        self.is_drought_tolerant = is_drought_tolerant
        self.is_flood_tolerant = is_flood_tolerant
        self.maturity_days = maturity_days
        self.potential_yield_t_ha = potential_yield_t_ha
        self.water_requirement_mm = water_requirement_mm
        self.input_costs_bdt_ha = input_costs_bdt_ha
        self.attributes: Dict[str, any] = {} # For additional characteristics
        if attributes:
            self.attributes.update(attributes)

    def __repr__(self):
        return f"RiceVariety(id='{self.variety_id}', name='{self.name}', season='{self.season.name}')"

# Example Varieties (to be expanded and loaded from data)
VARIETIES_DATA = {
    "brri_dhan28": RiceVariety(
        variety_id="brri_dhan28", name="BRRI dhan28", season=RiceSeason.BORO, 
        is_hyv=True, potential_yield_t_ha=6.0, maturity_days=140
    ),
    "brri_dhan29": RiceVariety(
        variety_id="brri_dhan29", name="BRRI dhan29", season=RiceSeason.BORO, 
        is_hyv=True, potential_yield_t_ha=7.0, maturity_days=160
    ),
    "brri_dhan47": RiceVariety(
        variety_id="brri_dhan47", name="BRRI dhan47", season=RiceSeason.BORO, 
        is_hyv=True, is_salt_tolerant=True, potential_yield_t_ha=5.5, maturity_days=150,
        attributes={"salinity_tolerance_ds_m": 8}
    ),
    "swarna": RiceVariety(
        variety_id="swarna", name="Swarna (MTU7029)", season=RiceSeason.AMAN, 
        is_hyv=True, potential_yield_t_ha=5.0, maturity_days=145
    ),
    "pajam": RiceVariety(
        variety_id="pajam", name="Pajam", season=RiceSeason.AMAN, 
        is_hyv=False, potential_yield_t_ha=3.5, maturity_days=150 # Traditional
    )
}

class Crop:
    """Represents a specific crop being grown on a plot in a given season."""
    def __init__(self, variety: RiceVariety, planting_date: Optional[str] = None, 
                 harvest_date: Optional[str] = None, actual_yield_t_ha: Optional[float] = None):
        self.variety = variety
        self.planting_date = planting_date # Should be datetime object eventually
        self.harvest_date = harvest_date   # Should be datetime object eventually
        self.current_growth_stage: Optional[str] = None # e.g., seedling, vegetative, flowering, maturity
        self.health_status: float = 1.0 # 0.0 (dead) to 1.0 (perfect health)
        self.actual_yield_t_ha = actual_yield_t_ha
        self.stress_factors: Dict[str, float] = {} # e.g., {'water_stress': 0.2, 'salinity_stress': 0.1}

    def update_growth(self, weather_conditions, soil_conditions, water_availability):
        """Placeholder for updating crop growth based on environmental factors."""
        # This will be a complex model involving crop growth simulation
        pass

    def apply_stress(self, stress_type: str, stress_level: float):
        """Applies a stress factor to the crop, potentially affecting health and yield."""
        self.stress_factors[stress_type] = self.stress_factors.get(stress_type, 0) + stress_level
        # Update health_status based on cumulative stress
        pass

    def __repr__(self):
        return f"Crop(variety='{self.variety.name}', stage='{self.current_growth_stage}')"
