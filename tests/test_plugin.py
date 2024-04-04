from cascadef.plugin import Node
import matplotlib.pyplot as plt
import networkx as nx
import datetime

def test_example_graph():
    ct = datetime.datetime.now()
    ts = ct.timestamp()

    user_1 = Node('User 1', ct)


    G = nx.DiGraph([('User 0','User 3' ), ('User 1', 'User 3'), ('User 2', 'User 4'), ('User 3', 'User 5'), ('User 3', 'User 6'), ('User 1', 'User 4'), ('User 5', 'User 6'), ('User 3' ,'User 4')])


    options = {
        "font_size": 12,
        "node_size": 3000,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 5,
        "width": 5,
    }


    # group nodes by column
    left_nodes = ['User 0']
    middle_nodes = ['User 1', 'User 2', 'User 3']
    right_nodes = ['User 4', 'User 5', 'User 6', 9]


    # set the position according to column (x-coord)
    pos = {n: (0, i) for i, n in enumerate(left_nodes)}
    pos.update({n: (1, i + 0.5) for i, n in enumerate(middle_nodes)})
    pos.update({n: (2, i + 0.5) for i, n in enumerate(right_nodes)})

    nx.draw_networkx(G, pos, **options)

    # Set margins for the axes so that nodes aren't clipped
    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")
    plt.show()