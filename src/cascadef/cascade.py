import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from cascadef.model import AbstractModelEnum
from abc import ABC, abstractmethod

class InfectionEvent:
    def __init__(self, vertex, state: AbstractModelEnum, time_stamp):
        self.vertex = vertex
        self.state = state
        self.time_stamp = time_stamp

    def get_vertex(self):
        return self.vertex
    
    def get_state(self) -> AbstractModelEnum:
        return self.state
    
    def get_time_stamp(self):
        return self.time_stamp

class Cascade:
    def __init__(self, graph: nx.Graph, infection_events: list[InfectionEvent]):
        self.graph = graph
        self.infection_events = infection_events  

    def get_graph_at_time(self, time) -> nx.Graph:
        graph = self.graph.copy()

        # get all infection events that happened before time
        infection_events = [event for event in self.infection_events if event.get_time_stamp() <= time]

        # infect nodes in the graph
        for event in infection_events:
            graph.nodes[event.get_vertex()]['state'] = event.get_state()

    def __get_node(self, vertex):
        return self.graph.nodes[vertex]

    def create_matplotlib_graph(self, time):
        # TODO: Implement matplotlib graph
        pass

    def animate(self):
        # TODO: Implement animation
        pass

class CascadeConstructor(ABC):
    @abstractmethod
    def create_cascade(graph, timeseries) -> Cascade:
        pass