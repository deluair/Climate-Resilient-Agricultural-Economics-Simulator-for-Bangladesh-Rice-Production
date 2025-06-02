from typing import Dict, Any
import json
import os

DEFAULT_SIMULATION_CONFIG = {
    "max_simulation_steps": 100, # e.g., 100 seasons or decision points
    "random_seed": 42,
    "use_synthetic_data": True,
    "synthetic_data_config": {
        "num_farmers": 200,
        "num_plots_per_farmer_avg": 2,
        "sim_duration_days": 365 * 10, # For weather generation, if daily steps
        "random_seed": 42 # Separate seed for data generator if needed
    },
    "data_loader_config": {
        "farmers_file": "data/real/farmers.csv",
        "plots_file": "data/real/farm_plots.json",
        "weather_file": "data/real/historical_weather.csv",
        "market_price_file": "data/real/market_prices.csv"
    },
    "reporting_options": {
        "output_directory": "results",
        "save_agent_data_interval": 10, # Save agent state every 10 steps
        "save_plot_data_interval": 10
    },
    "climate_model_config": {
        "historical_data_path": "data/climate/historical_weather.csv",
        "scenario_data_path": "data/climate/cmip6_rcp45_scenario.json",
        "selected_scenario": "RCP4.5"
    },
    "economic_model_config": {
        "default_interest_rate": 0.08,
        "subsidy_programs": [
            {"name": "fertilizer_subsidy", "type": "percentage", "value": 0.15} # 15% subsidy
        ]
    }
}

def get_default_config() -> Dict[str, Any]:
    """Returns a copy of the default simulation configuration."""
    return DEFAULT_SIMULATION_CONFIG.copy()

def load_config_from_json(file_path: str) -> Dict[str, Any]:
    """Loads simulation configuration from a JSON file.

    Args:
        file_path (str): The path to the JSON configuration file.

    Returns:
        Dict[str, Any]: The loaded configuration dictionary.
    
    Raises:
        FileNotFoundError: If the configuration file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    
    with open(file_path, 'r') as f:
        try:
            config = json.load(f)
            return config
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Error decoding JSON from {file_path}: {e.msg}", e.doc, e.pos)

def merge_configs(base_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
    """Merges two configurations, with override_config taking precedence for shared keys.
       Performs a deep merge for nested dictionaries.
    """
    merged = base_config.copy()
    for key, value in override_config.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = merge_configs(merged[key], value)
        else:
            merged[key] = value
    return merged

# Example usage:
if __name__ == '__main__':
    default_conf = get_default_config()
    print("Default Config:", json.dumps(default_conf, indent=2))

    # Example of creating a custom config file and loading it
    custom_config_content = {
        "max_simulation_steps": 50,
        "synthetic_data_config": {
            "num_farmers": 10 # Override nested value
        },
        "new_parameter": "custom_value"
    }
    custom_config_path = "custom_sim_config.json"
    with open(custom_config_path, 'w') as f:
        json.dump(custom_config_content, f, indent=2)
    
    print(f"\nLoading custom config from {custom_config_path}...")
    try:
        loaded_custom_conf = load_config_from_json(custom_config_path)
        print("Custom Config Loaded:", json.dumps(loaded_custom_conf, indent=2))
        
        final_config = merge_configs(default_conf, loaded_custom_conf)
        print("\nFinal Merged Config:", json.dumps(final_config, indent=2))

    except Exception as e:
        print(f"Error in example: {e}")
    finally:
        if os.path.exists(custom_config_path):
            os.remove(custom_config_path) # Clean up example file
