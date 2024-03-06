import pandas as pd
import networkx as nx

def load_data():
    data = pd.read_csv("data/Twitter_May-Aug.csv")
    return data
