from typing import Dict, List, Optional
from datetime import date
import pandas as pd # Placeholder, consider if pydantic is better for strict schemas

class WeatherParameters:
    """Represents daily weather parameters for a specific location and date."""
    def __init__(self,
                 record_date: date,
                 max_temp_c: Optional[float] = None, # Maximum temperature in Celsius
                 min_temp_c: Optional[float] = None, # Minimum temperature in Celsius
                 precipitation_mm: Optional[float] = None, # Precipitation in millimeters
                 humidity_percent: Optional[float] = None, # Relative humidity in percentage
                 solar_radiation_mj_m2: Optional[float] = None, # Solar radiation in MJ/m^2
                 wind_speed_m_s: Optional[float] = None, # Wind speed in m/s
                 station_id: Optional[str] = None):
        self.date = record_date
        self.max_temp_c = max_temp_c
        self.min_temp_c = min_temp_c
        self.precipitation_mm = precipitation_mm
        self.humidity_percent = humidity_percent
        self.solar_radiation_mj_m2 = solar_radiation_mj_m2
        self.wind_speed_m_s = wind_speed_m_s
        self.station_id = station_id

    def __repr__(self):
        return f"WeatherParameters(date={self.date}, station_id='{self.station_id}')"

class ClimateScenario:
    """Represents a climate change scenario (e.g., SSP2-4.5)."""
    def __init__(self, scenario_id: str, name: str, description: Optional[str] = None):
        self.scenario_id = scenario_id
        self.name = name
        self.description = description
        # Potentially store scenario-specific adjustment factors or time series data
        self.adjustment_factors: Dict[str, float] = {}

    def __repr__(self):
        return f"ClimateScenario(id='{self.scenario_id}', name='{self.name}')"

# Example: Historical weather data might be stored as a list of WeatherParameters objects
# or in a pandas DataFrame managed by ClimateManager.

# Placeholder for downscaled CMIP6 model data structure
# This could be a more complex object or a reference to a file path
# to be loaded by the ClimateManager.
class CMIP6Data:
    """Placeholder for CMIP6 model data."""
    def __init__(self, model_name: str, scenario: ClimateScenario, data_path: str):
        self.model_name = model_name
        self.scenario = scenario
        self.data_path = data_path # Path to NetCDF, CSV, or other format

    def load_data(self) -> Optional[pd.DataFrame]:
        """Placeholder for loading data. Actual implementation will depend on data format."""
        print(f"Loading data for {self.model_name} under {self.scenario.name} from {self.data_path}")
        # Example: if pd.read_csv(self.data_path)
        return None
