### Can you extract a cascade from just a networkx graph? Assuming the timestamps are in the nodes

No you need a series of events that happened on the graph as well.

For example if the graph is twitter users with edges being following one another, then one series of events could be tweets
containing a certain hashtag. If a tweet contains the hashtag then an infection event is created for the graph.

### Can you go over how to produce a cascade again?

**Cascade class**
- Graph
- array of vertex states in order by infection time
    - Vertex states could be anything but for now focus on "infected" and "available?" <- forgot what Magner called this one
    - If possible store the actual time value in the vertex state

### What is he looking for in the interface?

**CascadeConstructor**
+ create_cascade(graph, timeseries) -> Cascade:

### We had an idea about querying databases, is this necessary for the project?
For now don't worry about it

### Is there a specific type of data you want the data to be from? Or should it be up to the user?
Abstract data handling class
CascadeConstructor should not have to deal with data handling

In our example we are using an excel file so we can possibly create a class to handle that

### What are you looking for in the gui?
A graph displaying the cascade

He would like this to have a scroll bar of some sort which This bar should:
- allows you to select the nodes that were infected during a given time period.
- highlights the selected nodes on the graph
- be extendable i.e. you should be able to change the width of the bar to select a larger or smaller range of time.

### What timeseries take in again?

### Is it feasible to have a generic way to pull data from social media?
