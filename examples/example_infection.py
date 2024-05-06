import random
import networkx as nx
from cascadef.model import SIModel
from cascadef.graph import Graph, InfectionEvent, Node
from cascadef.cascade import CascadeConstructor, Cascade

# Create a graph
graph = Graph()

# Add nodes (people)
people = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah", "Ivan", "Julia"]
for person in people:
    node = Node(person, person, SIModel.SUSCEPTIBLE)
    graph.add_node(node)

# Add edges (relationships)
relationships = [
    ("Alice", "Bob"),
    ("Alice", "Charlie"),
    ("Bob", "David"),
    ("Charlie", "David"),
    ("David", "Eve"),
    ("Eve", "Frank"),
    ("Frank", "Grace"),
    ("Grace", "Hannah"),
    ("Hannah", "Ivan"),
    ("Ivan", "Julia"),
    ("Julia", "Alice")
]
for relationship in relationships:
    graph.add_edge_by_id(*relationship)

# Add random edges (daily contacts)
nx_graph = graph.get_networkx_graph()
num_edges = random.randint(1, 5)  # Number of edges to add (adjust as needed)
potential_edges = list(nx.non_edges(nx_graph))
added_edges = random.sample(potential_edges, num_edges)
nx_graph.add_edges_from(added_edges)

# Set an initial infected person
initial_infection = "Alice"

# Simulate infection spread over time
infected = set([initial_infection])  # Initial infected person
infection_events = [InfectionEvent(initial_infection, 0, SIModel.INFECTED)]
time_step = 0

while len(infected) < len(people):
    time_step += 1
    print(f"Time step: {time_step}")
    newly_infected = set()

    for person in infected:
        neighbors = graph.neighbors(person)
        for neighbor in neighbors:
            if neighbor not in infected and random.random() < 0.3:  # 30% chance of infection
                newly_infected.add(neighbor.get_id())
                print(f"{neighbor.get_id()} got infected from {person}")

    infected.update(newly_infected)
    infection_events.extend([InfectionEvent(person, time_step, SIModel.INFECTED) for person in newly_infected])
    print(f"Newly infected: {newly_infected}")

# Implement a custom cascade constructor
class ExampleInfectionPlugin(CascadeConstructor):
    def create_cascade(graph, timeseries) -> Cascade:
        return Cascade(graph, timeseries)

def print_currently_infected_at_time(cascade, time):
    nodes_in_state = cascade.get_nodes_in_state_at_time(time, SIModel.INFECTED)
    print("Currently infected nodes:{}, at time:{}".format([node.get_id() for node in nodes_in_state], time))
    cascade.create_matplotlib_graph(slider=True, time=0, node_size=1000)

cascade = ExampleInfectionPlugin.create_cascade(graph, infection_events)
print_currently_infected_at_time(cascade, 0)