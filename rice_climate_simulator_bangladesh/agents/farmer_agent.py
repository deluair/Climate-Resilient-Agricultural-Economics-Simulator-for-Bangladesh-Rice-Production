from typing import List, Dict, Optional
from uuid import uuid4

from .base_agent import BaseAgent
from agriculture.farm_plot import FarmPlot
from agriculture.crops import RiceVariety, RiceSeason, VARIETIES_DATA # For variety selection
# from ..economics.financial_model import HouseholdFinance # If a separate finance model exists

class FarmerAgent(BaseAgent):
    """
    Represents a farmer household agent in the simulation.
    Manages farm plots, makes cultivation decisions, and responds to economic
    and environmental conditions.
    """
    def __init__(self, agent_id: str = None,
                 household_id: str = None,
                 initial_capital_bdt: float = 50000.0,
                 farm_plots: Optional[List[FarmPlot]] = None,
                 age: int = 48,
                 education_years: int = 7,
                 farming_experience_years: int = 24,
                 risk_aversion_factor: float = 0.5, # 0 (risk-neutral) to 1 (highly risk-averse)
                 land_holding_category: str = "small", # e.g., marginal, small, medium, large
                 location_id: Optional[str] = None, # Link to an administrative unit ID
                 num_farm_plots: int = 0 # Expected number of farm plots from schema
                 ):
        super().__init__(agent_id)
        self.household_id = household_id if household_id else f"HH_{self.agent_id}"
        self.capital_bdt = initial_capital_bdt
        self.farm_plots: List[FarmPlot] = farm_plots if farm_plots else []
        self.age = age
        self.education_years = education_years
        self.num_farm_plots = num_farm_plots
        self.farming_experience_years = farming_experience_years
        self.risk_aversion_factor = risk_aversion_factor
        self.land_holding_category = land_holding_category # Could be an Enum
        self.location_id = location_id # e.g., Upazila ID

        self.expected_yields: Dict[str, float] = {} # variety_id -> expected_yield_t_ha
        self.expected_prices: Dict[str, float] = {} # rice_type -> expected_price_bdt_kg
        self.current_debt_bdt: float = 0.0
        self.subsidy_received_bdt: float = 0.0
        self.off_farm_income_bdt_per_year: float = 0.0 # Potential for diversification

    def add_farm_plot(self, plot: FarmPlot):
        if plot.owner_agent_id != self.agent_id:
            # Or assign it if it's being transferred
            print(f"Warning: Plot {plot.plot_id} owner mismatch. Assigning to {self.agent_id}.")
            plot.owner_agent_id = self.agent_id
        self.farm_plots.append(plot)

    def _select_rice_variety(self, plot: FarmPlot, season: RiceSeason, climate_outlook: dict, market_outlook: dict) -> Optional[RiceVariety]:
        """
        Decision logic for selecting a rice variety for a given plot and season.
        This is a placeholder for a more complex decision model.
        """
        available_varieties = [v for v_id, v in VARIETIES_DATA.items() if v.season == season]
        if not available_varieties:
            return None

        predicted_salinity = climate_outlook.get('avg_salinity_ds_m', 0)
        if predicted_salinity > 4: # Arbitrary threshold
            salt_tolerant_options = [v for v in available_varieties if v.is_salt_tolerant and v.attributes.get('salinity_tolerance_ds_m', 0) >= predicted_salinity]
            if salt_tolerant_options:
                return max(salt_tolerant_options, key=lambda v: v.potential_yield_t_ha)
        
        hyv_options = [v for v in available_varieties if v.is_hyv and v.input_costs_bdt_ha <= (self.capital_bdt / len(self.farm_plots) if self.farm_plots else self.capital_bdt)]
        if hyv_options:
            return max(hyv_options, key=lambda v: v.potential_yield_t_ha)
        
        if available_varieties:
            return max(available_varieties, key=lambda v: v.potential_yield_t_ha)
            
        return None

    def _make_cultivation_decisions(self, current_simulation_step: int, climate_conditions: dict, market_conditions: dict):
        """Decide what to plant on each plot for the upcoming season(s)."""
        if current_simulation_step % 3 == 0:
            current_season = RiceSeason.AUS
        elif current_simulation_step % 3 == 1:
            current_season = RiceSeason.AMAN
        else:
            current_season = RiceSeason.BORO
        
        print(f"Farmer {self.agent_id} making decisions for {current_season.name} at step {current_simulation_step}.")

        for plot in self.farm_plots:
            if plot.current_crop is None:
                climate_outlook_for_plot = climate_conditions.get(plot.plot_id, {}) 
                market_outlook_for_plot = market_conditions
                selected_variety = self._select_rice_variety(plot, current_season, climate_outlook_for_plot, market_outlook_for_plot)
                
                if selected_variety:
                    if self.capital_bdt >= selected_variety.input_costs_bdt_ha * plot.size_ha:
                        planting_date_str = f"Day {current_simulation_step*10}"
                        plot.plant_crop(selected_variety, planting_date_str, current_season)
                        self.capital_bdt -= selected_variety.input_costs_bdt_ha * plot.size_ha
                        print(f"  Farmer {self.agent_id} planted {selected_variety.name} on plot {plot.plot_id}. Capital left: {self.capital_bdt:.2f} BDT")
                    else:
                        print(f"  Farmer {self.agent_id} cannot afford to plant {selected_variety.name} on plot {plot.plot_id}.")
                else:
                    print(f"  Farmer {self.agent_id} could not select a suitable variety for plot {plot.plot_id} for {current_season.name}.")
            else:
                pass

    def _manage_finances(self, market_conditions: dict):
        pass

    def _adapt_strategies(self, climate_trends: dict, policy_changes: dict):
        pass

    def step(self, current_simulation_step: int, climate_conditions: dict, market_conditions: dict):
        print(f"--- Farmer Agent {self.agent_id} (Step {current_simulation_step}) ---")
        for plot in self.farm_plots:
            plot.update_plot_conditions(
                daily_weather=climate_conditions.get('weather', {}).get(plot.plot_id),
                hydrological_conditions=climate_conditions.get('hydrology', {}).get(plot.plot_id)
            )

        self._make_cultivation_decisions(current_simulation_step, climate_conditions, market_conditions)

        total_harvest_value = 0
        for plot in self.farm_plots:
            if plot.current_crop and plot.current_crop.current_growth_stage == "maturity_reached_placeholder":
                stress_impact = sum(plot.current_crop.stress_factors.values())
                yield_reduction_factor = max(0, 1 - stress_impact)
                actual_yield_t_ha = plot.current_crop.variety.potential_yield_t_ha * yield_reduction_factor
                harvested_crop_obj = plot.harvest_crop(f"Day {current_simulation_step*10 + 100}", actual_yield_t_ha)
                if harvested_crop_obj:
                    price_per_ton_bdt = market_conditions.get('rice_price_bdt_ton', {}).get(harvested_crop_obj.variety.variety_id, 30000)
                    revenue = harvested_crop_obj.actual_yield_t_ha * plot.size_ha * price_per_ton_bdt
                    self.capital_bdt += revenue
                    total_harvest_value += revenue
                    print(f"  Farmer {self.agent_id} sold {harvested_crop_obj.variety.name} from plot {plot.plot_id}. Revenue: {revenue:.2f} BDT. Capital: {self.capital_bdt:.2f} BDT")
        
        if total_harvest_value > 0:
            print(f"  Farmer {self.agent_id} total harvest income this step: {total_harvest_value:.2f} BDT")

        self._manage_finances(market_conditions)

        if current_simulation_step % 10 == 0:
             self._adapt_strategies(climate_conditions.get('trends',{}), market_conditions.get('policy_changes',{}))
        
        print(f"--- End Farmer Agent {self.agent_id} (Step {current_simulation_step}) ---")

    def __repr__(self):
        return f"FarmerAgent(id='{self.agent_id}', plots={len(self.farm_plots)}, capital={self.capital_bdt:.2f} BDT)"
