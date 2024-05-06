import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from abc import ABC, abstractmethod
from cascadef.graph import Graph, InfectionEvent, Node
from cascadef.model import AbstractModelEnum

class Cascade:
    """
    Represents a cascade in a graph. On creation, the cascade adds infection events to the nodes in the graph.

    Attributes:
        infection_events (list[InfectionEvent]): The list of infection events in the cascade.
        graph (Graph): The underlying graph.
    """
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
        """
        Returns the time of the last infection event.
        """
        if len(self.infection_events) == 0:
            return None
        return self.infection_events[-1].get_time_stamp()

    def get_start_time(self):
        """
        Returns the time of the first infection event.
        """
        if len(self.infection_events) == 0:
            return None
        return self.infection_events[0].get_time_stamp()

    def get_graph(self) -> Graph:
        """
        Returns the underlying graph.
        """
        return self.graph
    
    def get_node(self, id) -> Node:
        """
        Returns the node with the specified ID.

        Args:
            id (int): The ID of the node.

        Returns:
            Node: The node with the specified ID.
        """
        return self.graph.get_node(id)

    def get_infection_events(self) -> list[InfectionEvent]:
        """
        Returns the list of infection events in the cascade.
        """
        return self.infection_events

    def get_nodes_in_state_at_time(self, time, state: AbstractModelEnum) -> list[Node]:
        """
        Returns the nodes in a specific state at a given time.

        Args:
            time (int): The time to consider.
            state (AbstractModelEnum): The state to filter nodes by.

        Returns:
            list[Node]: The list of nodes in the specified state at the given time.
        """
        nodes_in_state = []
        for node in self.graph.get_nodes():
            if node.get_state_at_time(time) == state:
                nodes_in_state.append(node)
        return nodes_in_state

    def create_matplotlib_graph(self, time=None, slider=True, node_size=500, font_size=10, font_weight='bold', **kwargs):
        """
        Creates a matplotlib graph representation of the cascade.

        Args:
            time (int, optional): The time to visualize the cascade at. Defaults to the end time if not specified.
            slider (bool, optional): Whether to include a time slider. Defaults to True.
            node_size (int, optional): The size of the nodes in the graph. Defaults to 500.
            font_size (int, optional): The font size for node labels. Defaults to 10.
            font_weight (str, optional): The font weight for node labels. Defaults to 'bold'.
            **kwargs: Additional keyword arguments for graph layout and styling.
        """
        nx_graph = self.graph.get_networkx_graph()

        if time is None:
            time = self.get_end_time()

        if 'layout' in kwargs:
            layout = kwargs['layout']
        else:
            layout = nx.spring_layout(nx_graph, seed=43)

        fig, ax = plt.subplots()


        # Draw the graph
        def draw_graph(time):
            colors = [node.get_state_at_time(time).color() for node in nx_graph.nodes()]
            node_labels = {node: node.get_id() for node in nx_graph.nodes()}
            nx.draw(
                nx_graph, 
                pos=layout, 
                with_labels=True, 
                node_color=colors, 
                labels=node_labels, 
                node_size=node_size, 
                font_size=12, 
                font_weight=font_weight,
                ax=ax)

        draw_graph(time)


        if not slider or self.get_end_time() == self.get_start_time():
            plt.show()
            return

        # Create a slider widget
        slider_ax = plt.axes([0.2, 0.02, 0.6, 0.03])
        time_slider = Slider(slider_ax, 'Time', valmin=self.get_start_time(), valmax=self.get_end_time(), valinit=time, valstep=1, valfmt='%d')

        # Function to update the graph based on the slider value
        def update_graph(new_time):
            ax.clear()
            new_time = int(new_time)
            draw_graph(new_time)
            fig.canvas.draw_idle()

        # Connect the slider to the update_graph function
        time_slider.on_changed(update_graph)

        # Display the graph
        plt.show()

    def animate(self):
        """
        Animates the cascade.
        """
        # TODO: Implement animation
        pass

class CascadeConstructor(ABC):
    """
    Abstract base class for cascade constructors.
    """
    @abstractmethod
    def create_cascade(graph, timeseries) -> Cascade:
        """
        Creates a cascade from a graph and a time series.

        Args:
            graph (Graph): The underlying graph.
            timeseries (list): The time series data.

        Returns:
            Cascade: The constructed cascade.
        """
        pass