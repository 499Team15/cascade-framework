from cascadef.model import AbstractModelEnum
import networkx as nx

class Node:
    def __init__(self, value, time_stamp, content):
        self.value = value
        self.time_stamp = time_stamp
        self.infection_status = False
        self.content = content
    
    def get_value(self):
        return self.value

    def get_time_stamp(self):
        return self.time_stamp
    
    def set_time_stamp(self, value, time_stamp): 
        self.time_stamp = time_stamp

    def set_value(self, value):
        self.value = value

    def get_infection_status(self):
        return self.infection_status
    
    def infected(self):
        self.infection_status = True

class InfectionEvent:
    def __init__(self, node_id, time_stamp, state: AbstractModelEnum):
        self.vertex = node_id
        self.state = state
        self.time_stamp = time_stamp

    def get_node_id(self):
        return self.vertex
    
    def get_state(self) -> AbstractModelEnum:
        return self.state
    
    def get_time_stamp(self):
        return self.time_stamp

class InfectionNode:
    def __init__(self, id, value, starting_state: AbstractModelEnum):
        self.id = id
        self.value = value
        self.starting_state = starting_state
        self.infection_events = sorted([], key=lambda x: x.get_time_stamp())

    def get_value(self):
        return self.value

    def get_id(self):
        return self.id

    def add_infection_event(self, event: InfectionEvent):
        self.infection_events.append(event)

    def get_current_infection_state(self):
        if len(self.infection_events) == 0:
            return self.starting_state
        return self.infection_events[-1].get_state()

    def get_state_at_time(self, time):
        for event in reversed(self.infection_events):
            if event.get_time_stamp() <= time:
                return event.get_state()

        return self.starting_state

class Graph:
    def __init__(self) -> None:
        self.graph = nx.Graph()
        self.id_to_node = {}

    def add_node(self, node: InfectionNode):
        self.graph.add_node(node)
        self.id_to_node[node.get_id()] = node

    def add_edge(self, node1: InfectionNode, node2: InfectionNode, **attr):
        self.graph.add_edge(node1, node2, **attr)

    def add_edge_by_id(self, id1, id2, **attr):
        node1 = self.id_to_node[id1]
        node2 = self.id_to_node[id2]
        self.graph.add_edge(node1, node2, **attr)

    def get_node(self, id):
        return self.id_to_node.get(id, None)
    
    def get_networkx_graph(self):
        return self.graph