from abc import ABC, abstractmethod
from uuid import uuid4

class BaseAgent(ABC):
    """
    Abstract base class for all agents in the simulation.
    """
    def __init__(self, agent_id: str = None):
        self.agent_id = agent_id if agent_id else str(uuid4())

    @abstractmethod
    def step(self, current_time_step: int, climate_conditions: dict, market_conditions: dict):
        """
        Represents a single step or decision-making process for the agent
        in a given time period.

        Args:
            current_time_step (int): The current simulation step/year.
            climate_conditions (dict): Current climate data (e.g., weather, salinity).
            market_conditions (dict): Current market data (e.g., prices, subsidies).
        """
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}(id='{self.agent_id}')"
