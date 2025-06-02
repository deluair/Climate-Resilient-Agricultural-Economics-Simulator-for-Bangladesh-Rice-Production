from typing import Optional, Dict, List
from uuid import uuid4

# from ..geography.spatial_units import AdministrativeUnit # For location context
from .crops import Crop, RiceVariety, RiceSeason

class SoilProperties:
    """Represents soil characteristics of a farm plot."""
    def __init__(self, soil_type: str = "Loam", organic_matter_percent: float = 1.5,
                 ph: float = 6.5, salinity_ds_m: float = 1.0, # dS/m (deciSiemens per meter)
                 available_nitrogen_kg_ha: float = 100.0,
                 available_phosphorus_kg_ha: float = 20.0,
                 available_potassium_kg_ha: float = 150.0):
        self.soil_type = soil_type
        self.organic_matter_percent = organic_matter_percent
        self.ph = ph
        self.salinity_ds_m = salinity_ds_m # Current soil salinity
        self.initial_salinity_ds_m = salinity_ds_m # For tracking changes
        self.available_nitrogen_kg_ha = available_nitrogen_kg_ha
        self.available_phosphorus_kg_ha = available_phosphorus_kg_ha
        self.available_potassium_kg_ha = available_potassium_kg_ha
        self.water_holding_capacity_mm: float = 150 # Example, depends on soil type
        self.current_soil_moisture_mm: float = 100 # Current available water in root zone

    def update_salinity(self, change_ds_m: float):
        self.salinity_ds_m += change_ds_m
        self.salinity_ds_m = max(0, self.salinity_ds_m) # Salinity cannot be negative

    def update_soil_moisture(self, rainfall_mm: float, irrigation_mm: float, et_crop_mm: float):
        """Updates soil moisture based on water inputs and outputs."""
        self.current_soil_moisture_mm += rainfall_mm + irrigation_mm - et_crop_mm
        self.current_soil_moisture_mm = max(0, min(self.current_soil_moisture_mm, self.water_holding_capacity_mm))

    def __repr__(self):
        return f"SoilProperties(type='{self.soil_type}', salinity={self.salinity_ds_m:.2f} dS/m)"

class FarmPlot:
    """Represents an individual farm plot with specific characteristics."""
    def __init__(self, plot_id: str, owner_agent_id: str, size_ha: float,
                 # location: AdministrativeUnit, # Link to geographic unit
                 soil_properties: Optional[SoilProperties] = None,
                 initial_land_quality: float = 1.0 # 0 to 1, higher is better
                 ):
        self.plot_id = plot_id if plot_id else str(uuid4())
        self.owner_agent_id = owner_agent_id # ID of the FarmerAgent who owns/manages this plot
        self.size_ha = size_ha # Size of the plot in hectares
        # self.location = location # Geographic context
        self.soil = soil_properties if soil_properties else SoilProperties()
        self.land_quality = initial_land_quality # Can degrade or improve over time
        self.current_crop: Optional[Crop] = None
        self.cultivation_history: List[Dict] = [] # Record of past crops, yields, inputs
        self.is_irrigated: bool = False # Whether the plot has access to irrigation
        self.irrigation_type: Optional[str] = None # e.g., 'groundwater_stw', 'surface_canal'
        self.water_source_reliability: float = 1.0 # 0 to 1, higher is more reliable

    def plant_crop(self, variety: RiceVariety, planting_date: str, season: RiceSeason):
        if self.current_crop:
            print(f"Warning: Plot {self.plot_id} already has a crop: {self.current_crop.variety.name}. Cannot plant new crop.")
            return False
        if variety.season != season:
            print(f"Warning: Variety {variety.name} is for {variety.season.name}, not suitable for current {season.name}.")
            return False
        
        self.current_crop = Crop(variety=variety, planting_date=planting_date)
        print(f"Plot {self.plot_id}: Planted {variety.name} for {season.name} season on {planting_date}.")
        return True

    def harvest_crop(self, harvest_date: str, actual_yield_t_ha: float) -> Optional[Crop]:
        if not self.current_crop:
            print(f"Warning: No crop to harvest on plot {self.plot_id}.")
            return None
        
        harvested_crop = self.current_crop
        harvested_crop.harvest_date = harvest_date
        harvested_crop.actual_yield_t_ha = actual_yield_t_ha
        
        self.cultivation_history.append({
            'variety_id': harvested_crop.variety.variety_id,
            'season': harvested_crop.variety.season.name,
            'planting_date': harvested_crop.planting_date,
            'harvest_date': harvest_date,
            'yield_t_ha': actual_yield_t_ha,
            'stress_factors': harvested_crop.stress_factors.copy()
        })
        self.current_crop = None
        print(f"Plot {self.plot_id}: Harvested {harvested_crop.variety.name}, yield: {actual_yield_t_ha:.2f} t/ha.")
        return harvested_crop

    def apply_irrigation(self, amount_mm: float):
        if self.is_irrigated and self.current_crop:
            self.soil.update_soil_moisture(rainfall_mm=0, irrigation_mm=amount_mm, et_crop_mm=0) # ET handled separately
            print(f"Plot {self.plot_id}: Applied {amount_mm}mm of irrigation.")
        elif not self.is_irrigated:
            print(f"Plot {self.plot_id}: Cannot irrigate, plot is not set up for irrigation.")
        elif not self.current_crop:
            print(f"Plot {self.plot_id}: No crop to irrigate.")

    def update_plot_conditions(self, daily_weather, hydrological_conditions):
        """Update soil conditions, crop growth based on external factors."""
        # Update soil moisture from rainfall (ET will be part of crop model)
        # rainfall = daily_weather.precipitation_mm if daily_weather else 0
        # self.soil.update_soil_moisture(rainfall_mm=rainfall, irrigation_mm=0, et_crop_mm=0) 
        
        # Update soil salinity based on hydrological conditions (e.g., river salinity, groundwater)
        # self.soil.update_salinity(change_ds_m=hydrological_conditions.get('salinity_change', 0))
        
        if self.current_crop:
            # self.current_crop.update_growth(daily_weather, self.soil, self.water_source_reliability)
            # Apply stresses based on conditions
            # if self.soil.current_soil_moisture_mm < some_threshold:
            #     self.current_crop.apply_stress('water_stress', 0.1)
            # if self.soil.salinity_ds_m > self.current_crop.variety.attributes.get('salinity_tolerance_ds_m', 100):
            #     self.current_crop.apply_stress('salinity_stress', 0.2)
            pass

    def __repr__(self):
        return f"FarmPlot(id='{self.plot_id}', size={self.size_ha}ha, owner='{self.owner_agent_id}')"
