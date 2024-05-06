from abc import ABC, abstractmethod
from enum import Enum

class AbstractModelEnum(Enum):
    """
    Abstract base class for model enums.
    """
    @abstractmethod
    def color(self):
        """
        Returns the color associated with the enum value.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Returns the string representation of the enum value.
        """
        return self.name.capitalize()

class SIModel(AbstractModelEnum):
    """
    Enum representing the states in the Susceptible-Infected (SI) model.
    """
    SUSCEPTIBLE = "Susceptible"
    INFECTED = "Infected"
    
    def color(self):
        """
        Returns the color associated with the enum value.

        Returns:
            str: The color associated with the enum value.
        """
        if self == SIModel.SUSCEPTIBLE:
            return "cyan"
        elif self == SIModel.INFECTED:
            return "red"

class SIRModel(AbstractModelEnum):
    """
    Enum representing the states in the Susceptible-Infected-Recovered (SIR) model.
    """
    SUSCEPTIBLE = "Susceptible"
    INFECTED = "Infected"
    RECOVERED = "Recovered"
    
    def color(self):
        """
        Returns the color associated with the enum value.

        Returns:
            str: The color associated with the enum value.
        """
        if self == SIRModel.SUSCEPTIBLE:
            return "blue"
        elif self == SIRModel.INFECTED:
            return "red"
        elif self == SIRModel.RECOVERED:
            return "green"