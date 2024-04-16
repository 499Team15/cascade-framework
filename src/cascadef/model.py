from abc import ABC, abstractmethod
from enum import Enum

class AbstractModelEnum(Enum):
    @abstractmethod
    def get_state_color(self):
        pass

    @abstractmethod
    def __str__(self) -> str:
        return self.name.capitalize()

class SIModel(AbstractModelEnum):
    SUSCEPTIBLE = "Susceptible"
    INFECTED = "Infected"
    
    @staticmethod
    def color(self):
        if self == SIModel.SUSCEPTIBLE:
            return "blue"
        elif self == SIModel.INFECTED:
            return "red"

class SIRModel(AbstractModelEnum):
    SUSCEPTIBLE = "Susceptible"
    INFECTED = "Infected"
    RECOVERED = "Recovered"
    
    @staticmethod
    def color(self):
        if self == SIRModel.SUSCEPTIBLE:
            return "blue"
        elif self == SIRModel.INFECTED:
            return "red"
        elif self == SIRModel.RECOVERED:
            return "green"