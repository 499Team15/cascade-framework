from datetime import datetime
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from cascadef.model import AbstractModelEnum
from abc import ABC, abstractmethod

# VertexState: Infected or Susceptible
class VertexState:
    def __init__(self, vertex, state: AbstractModelEnum, time_stamp: datetime):
        self.vertex = vertex
        self.state = state
        self.time_stamp = time_stamp

    def get_vertex(self):
        return self.vertex
    
    def get_state(self) -> AbstractModelEnum:
        return self.state
    
    def get_time_stamp(self) -> datetime:
        return self.time_stamp

class Cascade:
    def __init__(self, graph: nx.Graph, vertex_states: list[VertexState]):
        self.graph = graph
        self.vertex_states = vertex_states
    
    def example_plot(self):
        fig, ax = plt.subplots()
        pos = nx.spring_layout(self.graph)
        nx.draw_networkx_nodes(self.graph, pos, ax=ax, node_color='lightgray')
        nx.draw_networkx_edges(self.graph, pos, ax=ax)
        nx.draw_networkx_labels(self.graph, pos, ax=ax)

        colors = {vs.vertex: vs.state.get_state_color() for vs in self.vertex_states[0]}
        node_colors = [colors.get(node, 'lightgray') for node in self.graph.nodes()]
        node_collection = ax.scatter(
            [pos[node][0] for node in self.graph.nodes()],
            [pos[node][1] for node in self.graph.nodes()],
            c=node_colors,
            s=100,
        )

        def update(frame):
            time_stamp = self.time_stamps[frame]
            colors = {vs.vertex: vs.state.get_state_color() for vs in self.vertex_states if vs.time_stamp <= time_stamp}
            node_colors = [colors.get(node, 'lightgray') for node in self.graph.nodes()]
            node_collection.set_color(node_colors)
            ax.set_title(f"Time: {time_stamp}")
            return node_collection,

        ani = FuncAnimation(fig, update, frames=len(self.time_stamps), interval=500, blit=True)
        plt.show()

class CascadeConstructor(ABC):
    @abstractmethod
    def create_cascade(graph, timeseries) -> Cascade:
        pass