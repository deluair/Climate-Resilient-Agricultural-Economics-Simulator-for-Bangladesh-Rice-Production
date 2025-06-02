from typing import List, Optional, Dict, Any
from datetime import date, datetime
from pydantic import BaseModel, Field

# Re-using or aligning with existing classes where possible, but Pydantic offers validation.

class WeatherRecordSchema(BaseModel):
    record_date: date
    station_id: str
    max_temp_c: Optional[float] = Field(None, description="Maximum daily temperature in Celsius")
    min_temp_c: Optional[float] = Field(None, description="Minimum daily temperature in Celsius")
    precipitation_mm: Optional[float] = Field(None, description="Daily precipitation in millimeters")
    humidity_percent: Optional[float] = Field(None, description="Average daily humidity in percentage")
    solar_radiation_mj_m2: Optional[float] = Field(None, description="Daily solar radiation in MJ/m^2")
    wind_speed_m_s: Optional[float] = Field(None, description="Average daily wind speed in m/s")

class SoilPropertiesSchema(BaseModel):
    soil_type: str = "Loam"
    organic_matter_percent: float = 1.5
    ph: float = 6.5
    salinity_ds_m: float = 1.0
    water_holding_capacity_mm: float = 150

class FarmPlotSchema(BaseModel):
    plot_id: str
    owner_agent_id: Optional[str] = None # Can be assigned later
    size_ha: float = Field(..., gt=0, description="Size of the plot in hectares")
    # location_admin_unit_id: str # Link to AdministrativeUnit ID
    # location_aez_id: str # Link to AgroEcologicalZone ID
    soil_properties: SoilPropertiesSchema = Field(default_factory=SoilPropertiesSchema)
    is_irrigated: bool = False
    irrigation_type: Optional[str] = None # e.g., 'groundwater_stw', 'surface_canal'
    initial_land_quality: float = Field(1.0, ge=0, le=1)

class FarmerProfileSchema(BaseModel):
    agent_id: str
    household_id: str
    initial_capital_bdt: float = Field(..., ge=0)
    age: int = Field(..., gt=0)
    education_years: int = Field(..., ge=0)
    farming_experience_years: int = Field(..., ge=0)
    risk_aversion_factor: float = Field(..., ge=0, le=1)
    land_holding_category: str # e.g., marginal, small, medium, large
    location_admin_unit_id: Optional[str] = None # e.g., Upazila ID
    num_farm_plots: int = Field(0, ge=0)
    attributes: Dict[str, Any] = Field(default_factory=dict)

class MarketPriceSchema(BaseModel):
    record_date: date
    crop_variety_id: str
    market_location_id: Optional[str] = None
    price_bdt_kg: float = Field(..., gt=0, description="Price in BDT per kilogram")
    price_bdt_ton: Optional[float] = Field(None, description="Price in BDT per ton")

class SimulationInputDataSchema(BaseModel):
    farmers: List[FarmerProfileSchema]
    farm_plots: List[FarmPlotSchema]
    historical_weather: List[WeatherRecordSchema] = []
    market_prices: List[MarketPriceSchema] = []
    # Could add climate scenarios, policy settings etc.
