# Cascade library

The Cascade Library is a Python package for modeling and visualizing cascade dynamics on graphs. It provides classes and methods to create graphs, define infection events, and simulate the spread of infections over time.

## Usage

### Creating a Graph

To create a graph, you can use the `Graph` class from the `cascadef.graph` module. Here's an example:

```python
from cascadef.graph import Graph, Node
from cascadef.model import SIRModel

# Create a new graph
graph = Graph()

# Create nodes with their initial states
node1 = Node(1, "Node 1", SIRModel.SUSCEPTIBLE)
node2 = Node(2, "Node 2", SIRModel.INFECTED)
node3 = Node(3, "Node 3", SIRModel.SUSCEPTIBLE)

# Add nodes to the graph
graph.add_node(node1)
graph.add_node(node2)
graph.add_node(node3)

# Add edges between nodes
graph.add_edge(node1, node2)
graph.add_edge(node2, node3)
```

## Defining Infection Events
Infection events represent the state changes of nodes at specific time steps. You can create infection events using the `InfectionEvent` class:

```python
from cascadef.graph import InfectionEvent
from cascadef.model import SIRModel

# Create infection events
event1 = InfectionEvent(1, 0, SIRModel.INFECTED)
event2 = InfectionEvent(2, 1, SIRModel.RECOVERED)
event3 = InfectionEvent(3, 2, SIRModel.INFECTED)
```

## Creating a Cascade
```python
from cascadef.cascade import Cascade

# Create a cascade
cascade = Cascade(graph, [event1, event2, event3])
```

or optionally implement the `CascadeConstructor` interface to better organize code

```python
from cascadef.cascade import CascadeConstructor

class CustomCascadeConstructor(CascadeConstructor):
    def create_cascade(self, graph, timeseries):
        # Custom logic to create infection events based on the graph and timeseries
        infection_events = ...
        
        # Create and return the cascade
        return Cascade(graph, infection_events)
```

## Models
The library supports different epidemic models, such as the SI (Susceptible-Infected) model and the SIR (Susceptible-Infected-Recovered) model. These models are defined in the cascadef.model module.


The available models are:
+ SIModel: Represents the Susceptible-Infected model.
    + States: SUSCEPTIBLE, INFECTED
    + Colors: Blue for SUSCEPTIBLE, Red for INFECTED


+ SIRModel: Represents the Susceptible-Infected-Recovered model.
    + States: SUSCEPTIBLE, INFECTED, RECOVERED
    + Colors: Blue for SUSCEPTIBLE, Red for INFECTED, Green for RECOVERED

You can extend the AbstractModelEnum class to define your own custom models.


## Developer Setup



### Installing and using PDM:

PDM is a package manager for python and it builds a virtual environment so
we can all use the same python packages.

```bash
pip install pdm
```

Then in the root of this project run

```bash
pdm install
```

An option in vscode should pop up to add an environment. Click that and choose the one with
".venv". If it does not show up try restarting vscode 

It gives us useful stuff like

```bash
pdm add matplotlib
```

And it will automatically add matplotlib to the teams environment, at least after the git changes are uploaded.

### Testing

If pdm was installed correctly you should be able to run

```bash
pytest
```

which will run all of the tests in the tests/ directory