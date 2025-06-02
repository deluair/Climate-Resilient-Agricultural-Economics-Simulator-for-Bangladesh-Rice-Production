import random
from datetime import date, timedelta
from typing import List, Dict, Optional
from uuid import uuid4

from .schemas import (
    WeatherRecordSchema, FarmPlotSchema, FarmerProfileSchema, 
    SoilPropertiesSchema, MarketPriceSchema, SimulationInputDataSchema
)
# Potentially use Faker for more realistic names, locations etc.
# from faker import Faker
# fake = Faker()

class SyntheticDataGenerator:
    """Generates synthetic data for the simulation based on defined schemas."""

    def __init__(self, random_seed: Optional[int] = None):
        if random_seed:
            random.seed(random_seed)
        # self.fake = Faker() # if using Faker

    def generate_farmer_profile(self, agent_id: str, household_id: str, admin_unit_id: Optional[str] = None) -> FarmerProfileSchema:
        return FarmerProfileSchema(
            agent_id=agent_id,
            household_id=household_id,
            initial_capital_bdt=random.uniform(20000, 200000),
            age=random.randint(25, 65),
            education_years=random.randint(0, 16),
            farming_experience_years=random.randint(5, 40),
            risk_aversion_factor=random.uniform(0.1, 0.9),
            land_holding_category=random.choice(["marginal", "small", "medium", "large"]),
            location_admin_unit_id=admin_unit_id if admin_unit_id else f"upazila_{random.randint(1,10)}",
            num_farm_plots=0 # Will be updated after plots are assigned
        )

    def generate_farm_plot(self, plot_id: str, owner_agent_id: Optional[str] = None) -> FarmPlotSchema:
        soil_salinity = random.uniform(0.5, 8.0) if random.random() < 0.3 else random.uniform(0.5, 2.5)
        return FarmPlotSchema(
            plot_id=plot_id,
            owner_agent_id=owner_agent_id,
            size_ha=random.uniform(0.1, 2.5),
            soil_properties=SoilPropertiesSchema(
                soil_type=random.choice(["Clay Loam", "Sandy Loam", "Silty Clay", "Loam"]),
                organic_matter_percent=random.uniform(0.5, 3.0),
                ph=random.uniform(5.5, 7.5),
                salinity_ds_m=soil_salinity
            ),
            is_irrigated=random.choice([True, False]),
            irrigation_type=random.choice([None, "groundwater_stw", "surface_canal", "llp"]) if True else None # Simplified
        )

    def generate_weather_record(self, record_date: date, station_id: str) -> WeatherRecordSchema:
        # Basic seasonality for temperature and precipitation
        month = record_date.month
        min_temp = 15 + 10 * (1 + random.uniform(-0.1, 0.1)) # Base min temp
        max_temp = 25 + 10 * (1 + random.uniform(-0.1, 0.1)) # Base max temp

        if 5 <= month <= 9: # Monsoon season (approx)
            precipitation = random.uniform(0, 50) if random.random() < 0.7 else 0 # Higher chance of rain
            min_temp += 5 
            max_temp += 3
        elif 11 <= month <= 2: # Winter
            precipitation = random.uniform(0, 5) if random.random() < 0.1 else 0
            min_temp -= 5
            max_temp -= 5
        else: # Other months
            precipitation = random.uniform(0, 15) if random.random() < 0.3 else 0
        
        min_temp = max(5, min_temp) # Floor temp
        max_temp = min(45, max(max_temp, min_temp + 2)) # Cap temp and ensure max > min

        return WeatherRecordSchema(
            record_date=record_date,
            station_id=station_id,
            max_temp_c=round(max_temp, 1),
            min_temp_c=round(min_temp, 1),
            precipitation_mm=round(precipitation,1),
            humidity_percent=round(random.uniform(60,95),1) if precipitation > 0 else round(random.uniform(40,80),1),
            solar_radiation_mj_m2=round(random.uniform(5, 25),1),
            wind_speed_m_s=round(random.uniform(0.5, 5),1)
        )

    def generate_market_price(self, record_date: date, crop_variety_id: str) -> MarketPriceSchema:
        base_price = 30 # BDT/kg
        price_fluctuation = base_price * random.uniform(-0.15, 0.15)
        price = base_price + price_fluctuation
        return MarketPriceSchema(
            record_date=record_date,
            crop_variety_id=crop_variety_id,
            price_bdt_kg=round(price, 2)
        )

    def generate_initial_simulation_data(
        self, 
        num_farmers: int = 100, 
        num_plots_per_farmer_avg: int = 2,
        num_weather_stations: int = 3,
        sim_start_date: date = date(2020, 1, 1),
        sim_duration_days: int = 365 * 3 # 3 years of daily data
    ) -> SimulationInputDataSchema:
        
        farmers: List[FarmerProfileSchema] = []
        farm_plots: List[FarmPlotSchema] = []
        plot_counter = 0

        for i in range(num_farmers):
            agent_id = f"farmer_{uuid4()}"
            hh_id = f"HH_{str(i+1).zfill(4)}"
            farmer = self.generate_farmer_profile(agent_id=agent_id, household_id=hh_id)
            farmers.append(farmer)
            
            num_plots_for_this_farmer = random.randint(max(1, num_plots_per_farmer_avg-1), num_plots_per_farmer_avg+1)
            farmer.num_farm_plots = num_plots_for_this_farmer
            for _ in range(num_plots_for_this_farmer):
                plot_id = f"plot_{uuid4()}"
                plot = self.generate_farm_plot(plot_id=plot_id, owner_agent_id=agent_id)
                farm_plots.append(plot)
                plot_counter +=1
        
        historical_weather: List[WeatherRecordSchema] = []
        for day_offset in range(sim_duration_days):
            current_date = sim_start_date + timedelta(days=day_offset)
            for station_num in range(num_weather_stations):
                station_id = f"station_{station_num + 1}"
                weather_record = self.generate_weather_record(record_date=current_date, station_id=station_id)
                historical_weather.append(weather_record)

        market_prices: List[MarketPriceSchema] = []
        # Example: generate weekly prices for a few rice varieties
        rice_varieties_for_market = ["brri_dhan28", "brri_dhan29", "swarna"]
        for day_offset in range(0, sim_duration_days, 7): # Weekly prices
            current_date = sim_start_date + timedelta(days=day_offset)
            for variety_id in rice_varieties_for_market:
                price_record = self.generate_market_price(record_date=current_date, crop_variety_id=variety_id)
                market_prices.append(price_record)

        return SimulationInputDataSchema(
            farmers=farmers,
            farm_plots=farm_plots,
            historical_weather=historical_weather,
            market_prices=market_prices
        )

# Example usage:
if __name__ == '__main__':
    generator = SyntheticDataGenerator(random_seed=42)
    initial_data = generator.generate_initial_simulation_data(num_farmers=5, num_plots_per_farmer_avg=1, sim_duration_days=30)
    
    print(f"Generated {len(initial_data.farmers)} farmers.")
    for farmer in initial_data.farmers:
        print(f"  {farmer.agent_id}, Plots: {farmer.num_farm_plots}, Capital: {farmer.initial_capital_bdt:.2f}")

    print(f"\nGenerated {len(initial_data.farm_plots)} farm plots.")
    for plot in initial_data.farm_plots:
        print(f"  {plot.plot_id}, Owner: {plot.owner_agent_id}, Size: {plot.size_ha} ha, Salinity: {plot.soil_properties.salinity_ds_m:.2f} dS/m")

    print(f"\nGenerated {len(initial_data.historical_weather)} weather records.")
    if initial_data.historical_weather:
        print(f"  Example weather: {initial_data.historical_weather[0]}")

    print(f"\nGenerated {len(initial_data.market_prices)} market price records.")
    if initial_data.market_prices:
        print(f"  Example price: {initial_data.market_prices[0]}")

    # To save to JSON (example):
    # with open("synthetic_simulation_input.json", "w") as f:
    #     f.write(initial_data.json(indent=2))
    # print("\nSaved synthetic data to synthetic_simulation_input.json")
