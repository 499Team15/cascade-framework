import pandas as pd
from cascadef import cascade
from cascadef.cascade import Cascade, CascadeConstructor
from cascadef.graph import Node, Graph, InfectionEvent
from cascadef.model import SIModel, AbstractModelEnum

class TestState(AbstractModelEnum):
    SUSCEPTIBLE = "Susceptible"
    INFECTED = "Infected"
    RECOVERED = "Recovered"

    def color(self):
        if self == TestState.SUSCEPTIBLE:
            return "blue"
        elif self == TestState.INFECTED:
            return "red"
        elif self == TestState.RECOVERED:
            return "green"

def test_abstract_state_enum():
    state = TestState.SUSCEPTIBLE
    assert state.color() == "blue"
    assert str(state) == "Susceptible"

class TestCascadeConstructor(CascadeConstructor):
    def create_cascade(self, graph, timeseries) -> Cascade:
        infection_events = []
        for id in timeseries:
            infection_events.append(InfectionEvent(id, pd.Timestamp("2021-01-01"), SIModel.INFECTED))
        
        return Cascade(graph, infection_events)

def test_cascade_constructor():
    G = Graph()
    G.add_node(Node(1, "hello world", SIModel.SUSCEPTIBLE))
    G.add_node(Node(2, "i like cats", SIModel.SUSCEPTIBLE))
    G.add_node(Node(3, "something else", SIModel.SUSCEPTIBLE))
    timeseries = [1, 2, 1]
    
    constructor = TestCascadeConstructor()
    cascade = constructor.create_cascade(G, timeseries)

    assert cascade.get_graph() == G

    assert G.get_node(1).get_current_infection_state() == SIModel.INFECTED
    assert cascade.get_node(1).get_current_infection_state() == SIModel.INFECTED
    assert cascade.get_node(2).get_current_infection_state() == SIModel.INFECTED
    assert cascade.get_node(3).get_current_infection_state() == SIModel.SUSCEPTIBLE

    assert cascade.get_node(1).get_state_at_time(pd.Timestamp("2020-01-01")) == SIModel.SUSCEPTIBLE
    assert cascade.get_node(1).get_state_at_time(pd.Timestamp("2022-01-01")) == SIModel.INFECTED

def test_create_cascade():
    G = Graph()
    cascade = Cascade(G, [])
    assert cascade.get_graph() == G