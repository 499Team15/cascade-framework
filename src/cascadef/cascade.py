import networkx as nx
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from cascadef.graph import Graph, InfectionEvent, Node
from cascadef.model import AbstractModelEnum

class Cascade:
    def __init__(self, graph: Graph, infection_events: list[InfectionEvent]):
        for event in infection_events:
            node = graph.get_node(event.get_node_id())
            if node is None:
                raise ValueError(f"Node with id {event.get_node_id()} not found in graph")

            node.add_infection_event(event)

        self.graph = graph
        self.infection_events = infection_events  

    def get_graph(self) -> Graph:
        return self.graph
    
    def get_node(self, id) -> Node:
        return self.graph.get_node(id)

    def get_infection_events(self) -> list[InfectionEvent]:
        return self.infection_events

    def get_nodes_in_state_at_time(self, time, state: AbstractModelEnum) -> list[Node]:
        nodes_in_state = []
        for node in self.graph.get_nodes():
            if node.get_state_at_time(time) == state:
                nodes_in_state.append(node)
        return nodes_in_state

    def create_matplotlib_graph(self, time):
        nx_graph = self.graph.get_networkx_graph()

        colors = [node.get_state_at_time(time).color() for node in nx_graph.nodes()]
        node_labels = {node: node.get_id() for node in nx_graph.nodes()}

        layout = nx.spring_layout(nx_graph, seed=43)

        # Draw the graph
        nx.draw(nx_graph, pos=layout, with_labels=True, node_color=colors, labels=node_labels, node_size=500, font_size=12, font_weight='bold')

        # Display the graph
        plt.show()

    def animate(self):
        # TODO: Implement animation
        pass

class CascadeConstructor(ABC):
    @abstractmethod
    def create_cascade(graph, timeseries) -> Cascade:
        pass