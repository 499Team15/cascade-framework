import networkx as nx
import pandas as pd
import pytest
from cascadef import cascade
from cascadef.cascade import Cascade, InfectionEvent, CascadeConstructor
from cascadef.node import Node
from cascadef.model import SIModel

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

class TestCascadeConstructor(CascadeConstructor):
    def create_cascade(self, graph, timeseries) -> Cascade:
        vertexstates = []
        for node in timeseries:
            vertexstates.append(InfectionEvent(node, SIModel.INFECTED, pd.Timestamp("2021-01-01")))

        return Cascade(graph, vertexstates)

def test_abstract_state_enum():
    state = TestState.SUSCEPTIBLE
    assert state.get_state_color() == "blue"
    assert str(state) == "Susceptible"

def test_vertex_state():
    vstate = InfectionEvent("A", TestState.SUSCEPTIBLE, pd.Timestamp("2021-01-01"))
    assert vstate.get_vertex() == "A"
    assert vstate.get_state() == TestState.SUSCEPTIBLE
    assert vstate.get_time_stamp() == pd.Timestamp("2021-01-01")

def test_cascade_constructor():
    G = nx.Graph()
    G.add_node(Node(1, None, "hi"))
    G.add_node(Node(2, None, "other"))
    G.add_node(Node(3, None, "something"))
    timeseries = [0, 2, 0]
    
    constructor = TestCascadeConstructor()
    cascade = constructor.create_cascade(G, timeseries)
            
def test_large_cascade():
    raise NotImplementedError

def test_very_large_cascade():
    raise NotImplementedError