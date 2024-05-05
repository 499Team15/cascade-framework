import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
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

        # sort infection events by time
        self.infection_events = sorted(infection_events, key=lambda x: x.get_time_stamp())
        self.graph = graph

    def get_end_time(self):
        ''' Returns the time of the last infection event '''
        return self.infection_events[-1].get_time_stamp()

    def get_start_time(self):
        ''' Returns the time of the first infection event '''
        return self.infection_events[0].get_time_stamp()

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

    def create_matplotlib_graph(self, time=None, slider=True, **kwargs):
        nx_graph = self.graph.get_networkx_graph()

        if time is None:
            time = self.get_end_time()

        if 'layout' in kwargs:
            layout = kwargs['layout']
        else:
            layout = nx.spring_layout(nx_graph, seed=43)

        colors = [node.get_state_at_time(time).color() for node in nx_graph.nodes()]
        node_labels = {node: node.get_id() for node in nx_graph.nodes()}

        fig, ax = plt.subplots()

        # Draw the graph
        nx.draw(nx_graph, pos=layout, with_labels=True, node_color=colors, labels=node_labels, node_size=500, font_size=12, font_weight='bold', ax=ax)

        if not slider:
            plt.show()
            return

        # Create a slider widget
        slider_ax = plt.axes([0.2, 0.02, 0.6, 0.03])
        time_slider = Slider(slider_ax, 'Time', valmin=self.get_start_time(), valmax=self.get_end_time(), valinit=time, valstep=1, valfmt='%d')

        # Function to update the graph based on the slider value
        def update_graph(new_time):
            new_time = int(new_time)
            colors = [node.get_state_at_time(new_time).color() for node in nx_graph.nodes()]
            nx.draw(nx_graph, pos=layout, with_labels=True, node_color=colors, labels=node_labels, node_size=500, font_size=12, font_weight='bold', ax=ax)
            fig.canvas.draw_idle()

        # Connect the slider to the update_graph function
        time_slider.on_changed(update_graph)

        # Display the graph
        plt.show()

    def animate(self):
        # TODO: Implement animation
        pass

class CascadeConstructor(ABC):
    @abstractmethod
    def create_cascade(graph, timeseries) -> Cascade:
        pass