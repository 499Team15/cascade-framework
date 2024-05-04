import networkx as nx
import random
from cascadef.cascade import CascadeConstructor, Cascade, InfectionEvent
from cascadef.model import SIModel

# Create a graph
graph = nx.Graph()

# Add nodes (people)
people = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah", "Ivan", "Julia"]
for person in people:
    graph.add_node(person)

# Add edges (daily contacts)
graph.add_edge("Alice", "Bob")
graph.add_edge("Alice", "Charlie")
graph.add_edge("Bob", "David")
graph.add_edge("Charlie", "Eve")
graph.add_edge("Eve", "Frank")
graph.add_edge("Frank", "Grace")
graph.add_edge("Grace", "Hannah")
graph.add_edge("Hannah", "Ivan")
graph.add_edge("Ivan", "Julia")

# Add random edges (daily contacts)
num_edges = random.randint(5, 15)  # Number of edges to add (adjust as needed)
potential_edges = list(nx.non_edges(graph))
added_edges = random.sample(potential_edges, num_edges)
graph.add_edges_from(added_edges)

# Set an initial infected person
initial_infection = "Alice"

# Simulate infection spread over time
infected = set([initial_infection])
time_step = 0

while len(infected) < len(people):
    time_step += 1
    print(f"Time step: {time_step}")
    newly_infected = set()

    for person in infected:
        neighbors = graph.neighbors(person)
        for neighbor in neighbors:
            if neighbor not in infected and random.random() < 0.5:  # 50% chance of infection
                newly_infected.add(neighbor)
                print(f"{neighbor} got infected from {person}")

    infected.update(newly_infected)
    print(f"Currently infected: {', '.join(infected)}\n")

# Implement a custom cascade constructor
class ExampleCascade(CascadeConstructor):
    def create_cascade(graph, timeseries) -> Cascade:
        vertex_states = []
        for time, infected in enumerate(timeseries):
            for person in infected:
                state = SIModel.INFECTED if time > 0 else SIModel.SUSCEPTIBLE
                vertex_states.append(InfectionEvent(person, state, time))
        return Cascade(graph, vertex_states)

cascade = ExampleCascade.create_cascade(graph, infected)
cascade.example_plot()