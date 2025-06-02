# Climate-Resilient Agricultural Economics Simulator for Bangladesh Rice Production

This project simulates the agricultural economics of rice production in Bangladesh, with a focus on understanding and enhancing climate resilience. It employs an agent-based modeling approach to capture farmer decision-making and interactions within a dynamic environment.

## Key Features

* **Modular Design**: Core components like agents, agriculture, climate, economics, and the simulation engine are organized into distinct modules for clarity and extensibility.
* **Agent-Based Modeling**: Simulates individual farmer agents making decisions based on their profiles, economic conditions, and environmental factors.
* **Climate Impact Simulation**: Designed to incorporate climate data and scenarios to assess their impact on rice production.
* **Data-Driven**: Utilizes Pydantic for schema validation and supports both synthetic data generation and integration of real-world datasets.
* **Configurable Simulation**: Allows customization of simulation parameters through configuration files.

## Project Structure

The project is organized into the following main directories and files:

```text
rice_climate_simulator_bangladesh/
├── agents/                   # Agent definitions (e.g., FarmerAgent)
├── agriculture/              # Agricultural models (e.g., Crop, FarmPlot, RiceSeason)
├── climate/                  # Climate data models and processing (Placeholder)
├── data_management/          # Data schemas (Pydantic), synthetic data generator, data loaders
├── economics/                # Economic models (Placeholder)
├── geography/                # Geographical data and models (Placeholder)
├── hydrology/                # Hydrological models (Placeholder)
├── policy/                   # Policy intervention models (Placeholder)
├── reporting_analytics/      # Simulation output, reporting, and analysis tools (Placeholder)
├── simulation_core/          # Core simulation engine, configuration management
├── tests/                    # Unit and integration tests (Placeholder)
├── utils/                    # Utility functions and common tools
├── visualization/            # Visualization scripts (Placeholder)
├── data/                     # Data files (synthetic, real, config)
│   ├── config/
│   │   └── default_simulation_config.json
│   ├── synthetic/
│   └── real/ (Placeholder for actual datasets)
├── results/                  # Directory for simulation outputs (created at runtime)
├── main.py                   # Main entry point to run the simulation
├── requirements.txt          # Project dependencies
├── README.md                 # This file
└── .gitignore                # Specifies intentionally untracked files that Git should ignore
```

## Setup and Installation

1. **Prerequisites**:
   * Python 3.10 or higher (Python 3.12 used during development).
   * Git for cloning the repository.

2. **Clone the Repository**:

   ```bash
    git clone https://github.com/deluair/Climate-Resilient-Agricultural-Economics-Simulator-for-Bangladesh-Rice-Production.git
    cd Climate-Resilient-Agricultural-Economics-Simulator-for-Bangladesh-Rice-Production/rice_climate_simulator_bangladesh
   ```

3. **Create a Virtual Environment (Recommended)**:

   ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    # source venv/bin/activate
   ```

4. **Install Dependencies**:

   ```bash
    pip install -r requirements.txt
   ```

## How to Run the Simulation

To run the simulation, navigate to the `rice_climate_simulator_bangladesh` directory (if you are in the parent `Climate-Resilient-Agricultural-Economics-Simulator-for-Bangladesh-Rice-Production` directory, `cd rice_climate_simulator_bangladesh`) and execute the `main.py` script:

```bash
python main.py
```

This will run the simulation using the default configuration specified in `data/config/default_simulation_config.json` with quick test overrides from `main.py`.

### Custom Configuration (Future)

(Instructions will be added on how to use a custom configuration file via command-line arguments.)

## Core Modules Overview

* **`agents`**: Defines the behavior and attributes of different agent types in the simulation, primarily `FarmerAgent`.
* **`agriculture`**: Contains models for crops (e.g., `RiceVariety`), farm plots (`FarmPlot`), and agricultural seasons (`RiceSeason`).
* **`data_management`**: Manages data structures using Pydantic schemas (`schemas.py`) and includes a `SyntheticDataGenerator` for creating initial simulation data.
* **`simulation_core`**: Houses the `SimulationEngine` which orchestrates the simulation, manages simulation steps, and handles configuration loading (`config.py`).
* **`main.py`**: The main script to initialize and run the simulation.

## Data Handling

* **Schemas**: Pydantic schemas in `data_management/schemas.py` define the structure and validation rules for various data entities (e.g., farmer profiles, plot details).
* **Synthetic Data**: `data_management/synthetic_data_generator.py` is used to generate initial data for farmers and farm plots when `use_synthetic_data` is true in the configuration.
* **Real Data**: The structure allows for future integration of real-world datasets for climate, market prices, etc. (Placeholder files in `data/real/`).

## Contributing

(Details on how to contribute to the project will be added here.)

## License

This project is licensed under the MIT License. See the `LICENSE` file for details (To be added).
