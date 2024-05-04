import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from cascadef.graph import Graph, Node, InfectionEvent
from cascadef.model import AbstractModelEnum, SIModel
import networkx as nx
import matplotlib.pyplot as plt
from cascadef.cascade import Cascade, CascadeConstructor

class TwitterHashtagPlugin(CascadeConstructor):
    def __init__(self, criteria):
        self.criteria = criteria

    def create_cascade(self, graph, df: pd.DataFrame) -> Cascade:
        infection_events= []
        for index, row in df.iterrows():
            if self.criteria in row['text']:
                # Create InfectionEvent
                event = InfectionEvent(node_id=row['username'], time_stamp=row['created_at'], state=SIModel.INFECTED)
                infection_events.append(event)

        return Cascade(graph, infection_events)

class FileSearchApp:
    def __init__(self, master):
        self.master = master
        self.master.title("File Search")
        self.master.geometry("800x350")  # Set the window size

        self.label_file = tk.Label(master, text="Select a CSV or Excel file:")
        self.label_file.grid(row=0, column=0, padx=10, pady=10)

        self.label_nodes = tk.Label(master, text="Number of Nodes:")
        self.label_nodes.grid(row=1, column=0, padx=10, pady=10)

        self.entry_nodes = tk.Entry(master)
        self.entry_nodes.grid(row=1, column=1, padx=10, pady=10)

        self.label_criteria = tk.Label(master, text="Infection Criteria:")
        self.label_criteria.grid(row=2, column=0, padx=10, pady=10)

        self.entry_criteria = tk.Entry(master)
        self.entry_criteria.grid(row=2, column=1, padx=10, pady=10)

        self.search_button = tk.Button(master, text="Search File", command=self.search_file)
        self.search_button.grid(row=3, column=0, padx=10, pady=10)

        self.cancel_button = tk.Button(master, text="Cancel", command=self.master.quit)
        self.cancel_button.grid(row=3, column=1, padx=10, pady=10)

        self.result_label = tk.Label(master, text="")
        self.result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.total_infection_label = tk.Label(master, text="Total Infection Events: 0")
        self.total_infection_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def search_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx;*.xls")])
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                    df = pd.read_excel(file_path)
                else:
                    raise ValueError("Unsupported file format.")

                required_columns = ['username', 'text', 'created_at']  # Required columns
                for col in required_columns:
                    if col not in df.columns:
                        raise ValueError(f"The file is missing the required '{col}' column.")

                try:
                    num_nodes = int(self.entry_nodes.get())
                    if num_nodes <= 0:
                        raise ValueError("Number of nodes must be a positive integer.")
                    unique_usernames = df['username'].unique()[:num_nodes]

                    # Slice the DataFrame to the first x rows
                    df = df.head(num_nodes)

                except ValueError:
                    raise ValueError("Please enter a valid number of nodes.")

                infection_criteria = self.entry_criteria.get()

                # Convert 'created_at' column to datetime format
                df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d')

                # Creating graph
                graph = Graph()

                # Create nodes
                for username in unique_usernames:
                    node = Node(id=username, value=None, starting_state=SIModel.SUSCEPTIBLE)
                    graph.add_node(node)

                # Create instance of TwitterHashtagPlugin
                plugin = TwitterHashtagPlugin(criteria=infection_criteria)

                # Call create_cascade method
                cascade = plugin.create_cascade(graph, df)
                self.total_infection_label.config(text=f"Total Infection Events: {len(cascade.get_infection_events())}")

                # Display graph
                self.display_graph(graph.get_networkx_graph())

            except pd.errors.ParserError:
                messagebox.showerror("Error", "Error parsing the file. Please make sure it's a valid CSV or Excel file.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception:
                messagebox.showerror("Error", "An unexpected error occurred.")

    def display_graph(self, graph):
        plt.figure(figsize=(8, 6))
        pos = nx.random_layout(graph)  # Use random layout for positioning nodes
        node_labels = {node: node.get_id() for node in graph.nodes}  # Create a dictionary mapping nodes to their IDs
        nx.draw(graph, pos, labels=node_labels, with_labels=True, node_color=[node.starting_state.color() for node in graph.nodes], node_size=500)
        plt.title("User Infection Network")
        plt.show()

def main():
    root = tk.Tk()
    app = FileSearchApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
