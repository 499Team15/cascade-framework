import tkinter as tk
from tkinter import filedialog, messagebox
import re
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from cascadef import node as Node

def create_graph(df):
    G = nx.Graph()
    nodes_dict = {}
    node_connections = {}  # Track the number of connections for each node
    
    for index, row in df.iterrows():
        username = row['username']
        text = row['text']
        created_at = datetime.strptime(row['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d')
        
        if username not in nodes_dict:
            node = Node.Node(username, created_at, text)
            nodes_dict[username] = node
            G.add_node(node, label=username)  # Assigning username as label
            node_connections[username] = 0  # Initialize connection count for the node
        else:
            node = nodes_dict[username]
        
        # Connect to the first three encountered nodes
        for existing_node in G.nodes:
            if existing_node != node and node_connections[username] < 3 and not G.has_edge(node, existing_node):
                G.add_edge(node, existing_node, color='blue')
                node_connections[username] += 1
        
        if "booktwt" in text.lower() and created_at <= selected_date.strftime('%Y-%m-%d'):
            node.infected()

    return G

def draw_graph(G):
    pos = nx.random_layout(G)
    edge_colors = [G[u][v]['color'] for u,v in G.edges()]
    node_colors = ['red' if node.infection_status else 'blue' for node in G.nodes()]
    node_sizes = [300 if node.infection_status else 5 for node in G.nodes()]  
    red_nodes_count = sum(1 for node in G.nodes() if node.infection_status)
    nx.draw(G, pos, with_labels=False, node_color=node_colors, 
            edge_color=edge_colors, node_size=5, width=.1)
    
    min_x = min(pos[node][0] for node in pos)
    max_x = max(pos[node][0] for node in pos)
    min_y = min(pos[node][1] for node in pos)
    max_y = max(pos[node][1] for node in pos)
    plt.text((min_x + max_x) / 2, min_y - 0.1 * (max_y - min_y), f"# of Infected Nodes {selected_date.strftime('%Y-%m-%d')}: {red_nodes_count}", fontsize=12, ha='center')
    plt.show()

def generate_network(filepath, df_head, start_at_end=False):
    try:
        # Read CSV into DataFrame
        if filepath.endswith('.csv'):
            if start_at_end:
                df = pd.read_csv(filepath).tail(df_head)
            else:
                df = pd.read_csv(filepath).head(df_head)
        elif filepath.endswith('.tsv'):
            if start_at_end:
                df = pd.read_csv(filepath, sep='\t').tail(df_head)
            else:
                df = pd.read_csv(filepath, sep='\t').head(df_head)
        elif filepath.endswith('.xlsx'):
            if start_at_end:
                df = pd.read_excel(filepath).tail(df_head)
            else:
                df = pd.read_excel(filepath).head(df_head)
        else:
            raise ValueError("Unsupported file format. Please select a CSV, TSV, or Excel file.")

        # Check if required columns are present
        required_columns = ['username', 'text', 'created_at']  # Update with your required column names
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            messagebox.showerror("Error", f"Missing columns: {', '.join(missing_columns)}")
            return

        # Create graph
        G = create_graph(df)

        # Draw graph
        draw_graph(G)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def on_generate_button_click():
    global selected_date
    selected_date_str = entry_date.get()

    if not re.match(r'\d{4}/\d{2}/\d{2}', selected_date_str):
        messagebox.showerror("Error", "Date format must be YYYY/MM/DD")
        return

    selected_date = datetime.strptime(selected_date_str, '%Y/%m/%d')

    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"),
                                                      ("TSV files", "*.tsv"),
                                                      ("Excel files", "*.xlsx")])
    if not filepath:
        return  # If no file selected, return

    df_head = int(entry_head.get())
    if df_head <= 0:
        raise ValueError("Head number must be a positive integer")

    start_at_end = dropdown_start_at.get() == "Start at End"

    generate_network(filepath, df_head, start_at_end)


# Create main window
root = tk.Tk()
root.title("Network Graph Generator")

# Set window size
root.geometry("600x400")  # Set the size to 600x400 pixels

# Create label for the date selection
label_date = tk.Label(root, text="Enter Date in Format: YYYY/MM/DD")
label_date.pack()

# Create entry for date input
entry_date = tk.Entry(root)
entry_date.pack()

# Create label for DataFrame Head Number
label_head = tk.Label(root, text="Number of Nodes to Display:")
label_head.pack()

# Create entry for DataFrame Head Number
entry_head = tk.Entry(root)
entry_head.pack()

# Create dropdown for start option
start_options = ["Start at Beginning", "Start at End"]
dropdown_start_at = tk.StringVar(root)
dropdown_start_at.set(start_options[0])  # Default value
dropdown_start_menu = tk.OptionMenu(root, dropdown_start_at, *start_options)
dropdown_start_menu.pack()

# Create button
button_generate = tk.Button(root, text="Generate network", command=on_generate_button_click, width=15)
button_generate.pack()

# Run Tkinter event loop
root.mainloop()
