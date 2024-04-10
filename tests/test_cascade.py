import networkx as nx
import pandas as pd
import pytest
from cascadef import cascade

class TestState(cascade.AbstractModelEnum):
    SUSCEPTIBLE = "Susceptible"
    INFECTED = "Infected"
    RECOVERED = "Recovered"

    def get_state_color(self):
        if self == TestState.SUSCEPTIBLE:
            return "blue"
        elif self == TestState.INFECTED:
            return "red"
        elif self == TestState.RECOVERED:
            return "green"



def test_abstract_state_enum():
    state = TestState.SUSCEPTIBLE
    assert state.get_state_color() == "blue"
    assert str(state) == "Susceptible"

def test_vertex_state():
    raise NotImplementedError

def test_cascade_constructor():
    raise NotImplementedError

def test_large_cascade():
    raise NotImplementedError

def test_very_large_cascade():
    raise NotImplementedError
