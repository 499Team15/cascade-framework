from cascadef.model import AbstractModelEnum
import networkx as nx

class InfectionEvent:
    """
    Represents an infection event for a node in the graph.

    Attributes:
        vertex (int): The ID of the node.
        state (AbstractModelEnum): The state of the node after the infection event.
        time_stamp (int): The time stamp of the infection event.
    """
    def __init__(self, node_id, time_stamp, state: AbstractModelEnum):
        self.vertex = node_id
        self.state = state
        self.time_stamp = time_stamp

    def get_node_id(self):
        """
        Returns the ID of the node.
        """
        return self.vertex
    
    def get_state(self) -> AbstractModelEnum:
        """
        Returns the state of the node after the infection event.
        """
        return self.state
    
    def get_time_stamp(self):
        """
        Returns the time stamp of the infection event.
        """
        return self.time_stamp

class Node:
    """
    Represents a node in the graph.

    Attributes:
        id (int): The ID of the node.
        value (Any): The value associated with the node.
        starting_state (AbstractModelEnum): The starting state of the node.
        infection_events (list[InfectionEvent]): The list of infection events that occurred on the node.
    """
    def __init__(self, id, value, starting_state: AbstractModelEnum):
        self.id = id
        self.value = value
        self.starting_state = starting_state
        self.infection_events = sorted([], key=lambda x: x.get_time_stamp())

    def get_value(self):
        """
        Returns the value associated with the node.
        """
        return self.value

    def get_id(self):
        """
        Returns the ID of the node.
        """
        return self.id

    def add_infection_event(self, event: InfectionEvent):
        """
        Adds an infection event to the node.

        Args:
            event (InfectionEvent): The infection event to add.
        """
        self.infection_events.append(event)

    def get_current_infection_state(self):
        """
        Returns the current infection state of the node.

        Returns:
            AbstractModelEnum: The current infection state.
        """
        if len(self.infection_events) == 0:
            return self.starting_state
        return self.infection_events[-1].get_state()

    def get_state_at_time(self, time):
        """
        Returns the infection state of the node at a specific time.

        Args:
            time (int): The time to get the infection state at.

        Returns:
            AbstractModelEnum: The infection state at the specified time.
        """
        for event in reversed(self.infection_events):
            if event.get_time_stamp() <= time:
                return event.get_state()

        return self.starting_state
    

class Graph:
    """
    Represents a graph.

    Attributes:
        graph (nx.Graph): The underlying NetworkX graph.
        id_to_node (dict): A mapping of node IDs to node objects.
    """
    def __init__(self) -> None:
        self.graph = nx.Graph()
        self.id_to_node = {}

    def add_node(self, node: Node):
        """
        Adds a node to the graph.

        Args:
            node (Node): The node to add.
        """
        self.graph.add_node(node)
        self.id_to_node[node.get_id()] = node

    def add_edge(self, node1: Node, node2: Node, **attr):
        """
        Adds an edge between two nodes in the graph.

        Args:
            node1 (Node): The first node.
            node2 (Node): The second node.
            **attr: Additional edge attributes.
        """
        self.graph.add_edge(node1, node2, **attr)

    def add_edge_by_id(self, id1, id2, **attr):
        """
        Adds an edge between two nodes specified by their IDs.

        Args:
            id1 (any): The ID of the first node.
            id2 (any): The ID of the second node.
            **attr: Additional edge attributes.
        """
        node1 = self.id_to_node[id1]
        node2 = self.id_to_node[id2]
        self.graph.add_edge(node1, node2, **attr)

    def neighbors(self, id):
        """
        Returns the neighbors of a node specified by its ID.

        Args:
            id (int): The ID of the node.

        Returns:
            list[Node]: The list of neighboring nodes.
        """
        node = self.id_to_node.get(id, None)
        if node is not None:
            return self.graph.neighbors(node)
        return []

    def get_nodes(self):
        """
        Returns a node view of the graph, see NetworkX documentation for more details.
        """
        return self.graph.nodes

    def get_node(self, id):
        """
        Returns the node with the specified ID.

        Args:
            id (any): The ID of the node.

        Returns:
            Node: The node with the specified ID, or None if not found.
        """
        return self.id_to_node.get(id, None)
    
    def get_networkx_graph(self):
        """
        Returns the underlying NetworkX graph.
        """
        return self.graph