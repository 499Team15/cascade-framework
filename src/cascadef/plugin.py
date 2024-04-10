import networkx as nx
import matplotlib.pyplot as plt
import datetime
from abc import ABC, abstractmethod
from networkx import Graph
from cascadef.cascade import Cascade

class Plugin(ABC):
    @abstractmethod
    def create_graph(self, data) -> nx.Graph:
        pass

    # not sure if this is necessary
    # possibly used to create 
    @abstractmethod
    def process(self, graph: nx.Graph) -> nx.Graph:
        pass

    # provide a default implementation that should work for most plugins
    def create_cascade(self, graph: nx.Graph) -> Cascade:
        # self.process(graph)
        return Cascade

class TwitterPlugin(Plugin):
    def create_graph(self, twitterdata) -> nx.Graph:
        # use the twitter data to create a graph
        return nx.Graph
    def process(self, graph: nx.Graph) -> nx.Graph:
        # I think there is some processing needed to create the cascade
        return nx.Graph

    # add some additional methods that are specific to the Twitter plugin
    def plot_graph(self, graph: nx.Graph):
        nx.draw(graph, with_labels=True)
        plt.show()

