from typing import List, Dict, Optional, Any
import time
import random

from agents.base_agent import BaseAgent
from agents.farmer_agent import FarmerAgent # Specific agent type
from climate.climate_manager import ClimateManager
from data_management.synthetic_data_generator import SyntheticDataGenerator
from data_management.schemas import SimulationInputDataSchema
from agriculture.farm_plot import FarmPlot # For type hinting
# from ..economics.market_model import MarketModel # To be created

class SimulationEngine:
    """
    Manages the overall simulation lifecycle, including setup, agent management,
    and stepping through simulation time.
    """
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config if config else {}
        self.current_step: int = 0
        self.max_steps: int = self.config.get("max_simulation_steps", 10) # Example: 10 years/seasons
        
        self.agents: List[BaseAgent] = []
        self.farmer_agents: List[FarmerAgent] = []
        self.farm_plots_map: Dict[str, FarmPlot] = {} # plot_id -> FarmPlot object

        self.climate_manager: Optional[ClimateManager] = None
        # self.market_model: Optional[MarketModel] = None
        self.simulation_data: Optional[SimulationInputDataSchema] = None
        
        self._initialize_components()

    def _initialize_components(self):
        """Initializes core components like climate manager, market model, and loads initial data."""
        print("Initializing simulation components...")
        # Initialize ClimateManager (example with placeholder data path)
        # self.climate_manager = ClimateManager(historical_data_path="data/historical_weather.csv", 
        #                                     scenario_data_path="data/climate_scenarios.json")
        # Initialize MarketModel
        # self.market_model = MarketModel()
        
        # Load or generate initial simulation data
        use_synthetic_data = self.config.get("use_synthetic_data", True)
        if use_synthetic_data:
            print("Generating synthetic data for simulation...")
            data_gen_config = self.config.get("synthetic_data_config", {})
            generator = SyntheticDataGenerator(random_seed=data_gen_config.get("random_seed", 42))
            self.simulation_data = generator.generate_initial_simulation_data(
                num_farmers=data_gen_config.get("num_farmers", 50),
                num_plots_per_farmer_avg=data_gen_config.get("num_plots_per_farmer_avg", 2),
                sim_duration_days=data_gen_config.get("sim_duration_days", 365 * self.max_steps) # Match sim length
            )
        else:
            # Placeholder for loading real data using DataLoaders
            # data_loader_config = self.config.get("data_loader_config", {})
            # self.simulation_data = load_all_simulation_data(**data_loader_config)
            print("ERROR: Real data loading not yet implemented. Configure to use synthetic data.")
            raise NotImplementedError("Real data loading pathway is not yet implemented.")

        self._create_agents_and_plots()
        print("Simulation components initialized.")

    def _create_agents_and_plots(self):
        if not self.simulation_data:
            print("Error: Simulation data not loaded or generated.")
            return

        print(f"Creating {len(self.simulation_data.farmers)} farmer agents...")
        for farmer_schema in self.simulation_data.farmers:
            farmer = FarmerAgent(
                agent_id=farmer_schema.agent_id,
                household_id=farmer_schema.household_id,
                initial_capital_bdt=farmer_schema.initial_capital_bdt,
                age=farmer_schema.age,
                education_years=farmer_schema.education_years,
                farming_experience_years=farmer_schema.farming_experience_years,
                risk_aversion_factor=farmer_schema.risk_aversion_factor,
                land_holding_category=farmer_schema.land_holding_category,
                location_id=farmer_schema.location_admin_unit_id,
                num_farm_plots=farmer_schema.num_farm_plots # Pass the expected number of plots
            )
            self.agents.append(farmer)
            self.farmer_agents.append(farmer)

        print(f"Creating and assigning {len(self.simulation_data.farm_plots)} farm plots...")
        plot_assignment_map: Dict[str, List[FarmPlot]] = {farmer.agent_id: [] for farmer in self.farmer_agents}
        
        for plot_schema in self.simulation_data.farm_plots:
            # Create FarmPlot instance (actual object, not just schema)
            # Note: FarmPlot class from agriculture.farm_plot needs to be compatible or adapted
            plot = FarmPlot(
                plot_id=plot_schema.plot_id,
                owner_agent_id=plot_schema.owner_agent_id, # This should match a farmer_agent_id
                size_ha=plot_schema.size_ha,
                # soil_properties can be more complex, need to instantiate SoilProperties from schema
                initial_land_quality=plot_schema.initial_land_quality
            )
            # For simplicity, assigning soil properties directly if schema matches class structure
            # A more robust way would be: plot.soil = SoilProperties(**plot_schema.soil_properties.dict())
            plot.soil.soil_type = plot_schema.soil_properties.soil_type
            plot.soil.organic_matter_percent = plot_schema.soil_properties.organic_matter_percent
            plot.soil.ph = plot_schema.soil_properties.ph
            plot.soil.salinity_ds_m = plot_schema.soil_properties.salinity_ds_m
            plot.soil.water_holding_capacity_mm = plot_schema.soil_properties.water_holding_capacity_mm
            plot.is_irrigated = plot_schema.is_irrigated
            plot.irrigation_type = plot_schema.irrigation_type
            
            self.farm_plots_map[plot.plot_id] = plot
            if plot.owner_agent_id in plot_assignment_map:
                plot_assignment_map[plot.owner_agent_id].append(plot)
            else:
                print(f"Warning: Plot {plot.plot_id} has owner {plot.owner_agent_id} not in farmer list. Assigning to first farmer if available.")
                if self.farmer_agents:
                    plot.owner_agent_id = self.farmer_agents[0].agent_id
                    plot_assignment_map[self.farmer_agents[0].agent_id].append(plot)

        for farmer in self.farmer_agents:
            farmer.farm_plots = plot_assignment_map.get(farmer.agent_id, [])
            if len(farmer.farm_plots) != farmer.num_farm_plots: # num_farm_plots from schema
                 print(f"Warning: Farmer {farmer.agent_id} expected {farmer.num_farm_plots} plots, got {len(farmer.farm_plots)}.")

        print("Agents and plots created and assigned.")

    def run_step(self):
        """Runs a single step of the simulation."""
        if self.current_step >= self.max_steps:
            print("Maximum simulation steps reached.")
            return False # Indicate simulation should stop

        print(f"\n--- Simulation Step {self.current_step + 1} / {self.max_steps} ---")
        start_time = time.time()

        # 1. Get current climate conditions for the step
        # climate_conditions_for_step = self.climate_manager.get_conditions_for_step(self.current_step)
        climate_conditions_for_step = {
            "general": {"avg_temp_c": 28, "total_rainfall_mm": 150, "avg_salinity_ds_m": 1.2},
            "weather_for_plots": {plot_id: {"precipitation_mm": random.uniform(0,10)} for plot_id in self.farm_plots_map.keys() }, # Simplified
            "hydrology_for_plots": {plot_id: {"salinity_change": random.uniform(-0.1,0.1)} for plot_id in self.farm_plots_map.keys() }
        } # Placeholder

        # 2. Get current market conditions
        # market_conditions_for_step = self.market_model.get_market_state(self.current_step)
        market_conditions_for_step = {
            "rice_price_bdt_ton": {"brri_dhan28": 32000, "swarna": 28000, "default": 30000}
        } # Placeholder

        # 3. Agent actions (decision-making and execution)
        for agent in self.agents:
            agent.step(self.current_step, climate_conditions_for_step, market_conditions_for_step)
        
        # 4. Update environment (e.g., market clearing, aggregate environmental changes)
        # self.market_model.clear_market(self.agents) # Example
        # self.climate_manager.update_environment_state() # Example

        end_time = time.time()
        print(f"Step {self.current_step + 1} completed in {end_time - start_time:.4f} seconds.")
        self.current_step += 1
        return True # Indicate simulation can continue

    def run_simulation(self):
        """Runs the full simulation until max_steps is reached or a stop condition is met."""
        print("Starting simulation run...")
        print(f"Configuration: Max steps = {self.max_steps}, Agents = {len(self.agents)}")
        
        self.current_step = 0
        while self.run_step():
            pass
        
        print("\nSimulation run finished.")
        self.collect_results() # Placeholder for results collection

    def collect_results(self):
        """Collects and summarizes results from the simulation."""
        print("\n--- Collecting Simulation Results ---")
        total_capital = sum(fa.capital_bdt for fa in self.farmer_agents)
        print(f"Total capital of all farmers at end: {total_capital:.2f} BDT")
        
        for i, farmer in enumerate(self.farmer_agents):
            if i < 5: # Print details for first 5 farmers
                print(f"  Farmer {farmer.agent_id}: Capital = {farmer.capital_bdt:.2f} BDT, Plots = {len(farmer.farm_plots)}")
                for plot in farmer.farm_plots:
                    print(f"    Plot {plot.plot_id}: Size = {plot.size_ha} ha, Soil Salinity = {plot.soil.salinity_ds_m:.2f} dS/m")
                    if plot.cultivation_history:
                        print(f"      Last cultivation: {plot.cultivation_history[-1]['variety_id']}, Yield: {plot.cultivation_history[-1]['yield_t_ha']:.2f} t/ha")
        # Further results could include aggregate crop production, land use changes, economic indicators etc.
        # These would typically be written to files (CSV, JSON) or a database.

# Example usage (typically in main.py)
if __name__ == '__main__':
    import random # For placeholder in run_step
    sim_config = {
        "max_simulation_steps": 3, # Simulate 3 seasons/years for quick test
        "use_synthetic_data": True,
        "synthetic_data_config": {
            "num_farmers": 10,
            "num_plots_per_farmer_avg": 1,
            "random_seed": 123
        }
    }
    engine = SimulationEngine(config=sim_config)
    engine.run_simulation()
