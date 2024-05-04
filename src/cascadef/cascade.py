import networkx as nx
from abc import ABC, abstractmethod
from cascadef.graph import Graph, InfectionEvent, InfectionNode


class Cascade:
    def __init__(self, graph: Graph, infection_events: list[InfectionEvent]):
        for event in infection_events:
            node = graph.get_node(event.get_node_id())
            node.add_infection_event(event)

        self.graph = graph
        self.infection_events = infection_events  

    def get_graph(self) -> Graph:
        return self.graph
    
    def get_node(self, id) -> InfectionNode:
        return self.graph.get_node(id)

    def create_matplotlib_graph(self):
        # TODO: Implement matplotlib graph
        pass

    def animate(self):
        # TODO: Implement animation
        pass

class CascadeConstructor(ABC):
    @abstractmethod
    def create_cascade(graph, timeseries) -> Cascade:
        pass