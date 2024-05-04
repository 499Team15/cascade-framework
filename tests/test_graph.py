from cascadef.graph import Node, Graph
from cascadef.model import SIModel
from cascadef.cascade import InfectionEvent
import pandas as pd

def test_create_node():
    node = Node(1, 'content', SIModel.SUSCEPTIBLE)

def test_getters_and_setters():
    node = Node(1, 'content', SIModel.SUSCEPTIBLE)
    assert node.get_value() == 'content'
    assert node.get_id() == 1
    assert node.get_current_infection_state() == SIModel.SUSCEPTIBLE

    node.add_infection_event(InfectionEvent(1, 1, SIModel.INFECTED))
    assert node.get_current_infection_state() == SIModel.INFECTED

    node.add_infection_event(InfectionEvent(1, 2, SIModel.SUSCEPTIBLE))
    assert node.get_current_infection_state() == SIModel.SUSCEPTIBLE

    assert node.get_state_at_time(1) == SIModel.INFECTED
    assert node.get_state_at_time(2) == SIModel.SUSCEPTIBLE
    assert node.get_state_at_time(1.5) == SIModel.INFECTED


def test_graph():
    graph = Graph()
    node_1 = Node(1, 6, SIModel.SUSCEPTIBLE)
    node_2 = Node(2, 3, SIModel.SUSCEPTIBLE)

    graph.add_node(node_1)
    graph.add_node(node_2)

    assert graph.get_node(1) == node_1
    assert graph.get_node(2) == node_2

def test_graph_fail_access_node():
    graph = Graph()
    node_1 = Node(1, 6, SIModel.SUSCEPTIBLE)
    node_2 = Node(2, 3, SIModel.SUSCEPTIBLE)

    graph.add_node(node_1)
    graph.add_node(node_2)

    assert graph.get_node(3) == None

def test_infection_event():
    vstate = InfectionEvent("A", pd.Timestamp("2021-01-01"), SIModel.SUSCEPTIBLE)
    assert vstate.get_node_id() == "A"
    assert vstate.get_state() == SIModel.SUSCEPTIBLE
    assert vstate.get_time_stamp() == pd.Timestamp("2021-01-01")
