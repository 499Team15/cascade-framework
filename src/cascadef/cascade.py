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
    
    def create_gui():
        # TODO: Implement GUI 
        pass

class CascadeConstructor(ABC):
    @abstractmethod
    def create_cascade(graph, timeseries) -> Cascade:
        pass