# Main entry point for the Climate-Resilient Agricultural Economics Simulator for Bangladesh Rice Production
import sys
import os
print(f"DEBUG: Current Working Directory: {os.getcwd()}")
print(f"DEBUG: sys.path: {sys.path}\n")
import json
from simulation_core.engine import SimulationEngine
from simulation_core.config import get_default_config, load_config_from_json, merge_configs

def run_simulation(config_path: str = None):
    print("Initializing simulation...")

    # Load base configuration
    sim_config = get_default_config()

    # If a custom config path is provided, load and merge it
    if config_path:
        try:
            print(f"Loading custom configuration from: {config_path}")
            custom_config = load_config_from_json(config_path)
            sim_config = merge_configs(sim_config, custom_config)
            print("Custom configuration loaded and merged successfully.")
        except FileNotFoundError:
            print(f"Warning: Custom config file {config_path} not found. Using default configuration.")
        except json.JSONDecodeError as e:
            print(f"Error: Could not parse custom config file {config_path}: {e}. Using default configuration.")
    else:
        print("No custom configuration path provided. Using default simulation configuration.")

    # Example: Override specific parameters for a quick test run if no custom config
    if not config_path: # Apply these only if no custom config is loaded
        sim_config['max_simulation_steps'] = 5 # Short simulation for testing
        sim_config['synthetic_data_config']['num_farmers'] = 20
        sim_config['synthetic_data_config']['num_plots_per_farmer_avg'] = 1
        sim_config['synthetic_data_config']['random_seed'] = 12345
        print("Applied quick test overrides to default configuration.")

    print("\nFinal Simulation Configuration:")
    print(json.dumps(sim_config, indent=2))
    print("-"*50)

    # Initialize and run the simulation engine
    engine = SimulationEngine(config=sim_config)
    engine.run_simulation()

    print("\nSimulation run completed from main.py.")

if __name__ == "__main__":
    # To use a custom configuration file, provide its path:
    # custom_config_file = "config/my_simulation_settings.json" 
    # run_simulation(config_path=custom_config_file)
    
    # To run with default (and example test overrides):
    run_simulation()

