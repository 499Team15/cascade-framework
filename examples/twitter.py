import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from cascadef.graph import Graph, Node, InfectionEvent
from cascadef.model import AbstractModelEnum, SIModel
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


def open_file(root):
    # Retrieve the text entered in the criteria and nodes entry fields
    infection_criteria = criteria_entry.get()
    num_nodes = int(nodes_entry.get())

    if num_nodes <= 0:
        messagebox.showerror("Number of Nodes must be a positive integer")
    # Check if either criteria or nodes fields are empty
    if not infection_criteria or not num_nodes:
        messagebox.showerror("Error", "Please enter both Infection criteria and Number of Nodes.")
        return

    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filename:
        df = pd.read_csv(filename)
        required_columns = ['username', 'text', 'created_at']  # Required columns
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"The file is missing the required '{col}' column.")
        # Convert 'created_at' column to datetime
        df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d')
        df.sort_values(by='created_at', inplace=True)  # Sort DataFrame by 'created_at' column
        min_date = pd.to_datetime(df['created_at'].min())  
        max_date = pd.to_datetime(df['created_at'].max())  
        unique_usernames = df['username'].unique()

        selected_usernames = unique_usernames[:num_nodes]
        
        filtered_df = df[df['username'].isin(selected_usernames)]

        #Create and populate graph with states
        graph = Graph()
        for username in selected_usernames:
            node = Node(id=username, value=None, starting_state=SIModel.SUSCEPTIBLE)
            graph.add_node(node)
        plugin = TwitterHashtagPlugin(criteria=infection_criteria)
        
        # Call create_cascade method
        cascade = plugin.create_cascade(graph, filtered_df)

        graph_frame = tk.Frame(root)
        graph_frame.pack()


        # Embed the graph into the Tkinter window
        fig = plt.figure()

        cascade.create_matplotlib_graph(time=df['created_at'].min(), slider=False, node_size=50, font_size=6, no_show=True)
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        create_slider(min_date, max_date, root, graph_frame, cascade)

        


def create_slider(min_date, max_date, root, graph_frame, cascade: Cascade):
    def get_selected_date(value):
        selected_date = min_date + timedelta(days=value)
        label.config(text="Selected Date: " + selected_date.strftime("%Y-%m-%d"))
        
        #Clear current graph
        for widget in graph_frame.winfo_children():
            widget.destroy()
        
        #Draw new graph at selected date
        fig = plt.figure()
        cascade.create_matplotlib_graph(time=selected_date.strftime("%Y-%m-%d"), slider=False, node_size=50, font_size=6)
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        num_of_infected_label.config(text=f"Number of Nodes Infected At Current Time {len(cascade.get_nodes_in_state_at_time(selected_date.strftime("%Y-%m-%d"), SIModel.INFECTED))}")
      


    #Helper for changing date with slider
    def slider_changed(event):
        value = int(slider.get())
        get_selected_date(value)

    #Handles manual date entry
    def manual_date_change(event=None):
        input_date_str = date_entry.get()
        #Ensure date is valid fromat and within boundaries
        try:
            input_date = pd.to_datetime(input_date_str)  

            if min_date <= input_date <= max_date:
                #Set Slider Position
                days_diff = (input_date - min_date).days
                slider.set(days_diff)
                label.config(text="Selected Date: " + input_date.strftime("%Y-%m-%d"))

                #Clear current graph and draw new one at date
                for widget in graph_frame.winfo_children():
                    widget.destroy()

                fig = plt.figure()
                cascade.create_matplotlib_graph(time=input_date.strftime("%Y-%m-%d"), slider=False, node_size=50, font_size=6)
                canvas = FigureCanvasTkAgg(fig, master=graph_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                
                num_of_infected_label.config(text=f"Number of Nodes Infected At Current Time {len(cascade.get_nodes_in_state_at_time(input_date.strftime("%Y-%m-%d"), SIModel.INFECTED))}")

            else:
                raise ValueError
            label_error.config(text="")
            date_entry.delete(0, tk.END)  # Clear entry field
        except ValueError:
            label_error.config(text="Not a valid date", fg="red")

    def on_entry_key_press(event):
        if event.keysym == 'Return':
            manual_date_change()

    label_frame = tk.Frame(root)
    label_frame.pack(padx=10, pady=10)

    label = tk.Label(label_frame, text="")
    label.pack(padx=10, pady=10)
    label.config(text="Selected Date: " + min_date.strftime("%Y-%m-%d"))


    date_frame = tk.Frame(root)
    date_frame.pack(padx=10, pady=10)

    date_label = tk.Label(date_frame, text=f"Enter Date or Use Slider ({min_date.strftime("%Y-%m-%d")} - {max_date.strftime("%Y-%m-%d")}):")
    date_label.grid(row=0, column=0)

    date_entry = tk.Entry(date_frame)
    date_entry.grid(row=0, column=1)
    date_entry.bind("<Return>", on_entry_key_press)

    select_button = tk.Button(date_frame, text="Select Date", command=manual_date_change)
    select_button.grid(row=0, column=2)

    num_of_infected_frame = tk.Frame(root)
    num_of_infected_frame.pack(padx=10, pady=10)

    num_of_infected_label = tk.Label(num_of_infected_frame, text=f"Number of Infected Nodes at Current Time: {len(cascade.get_nodes_in_state_at_time(min_date.strftime("%Y-%m-%d"), SIModel.INFECTED))}")
    num_of_infected_label.grid(row=0, column=0)

    nodes_count_frame = tk.Frame(root)
    nodes_count_frame.pack(padx=10, pady=10)

    nodes_count_label = tk.Label(nodes_count_frame, text=f"Nodes: Visualized: {len(cascade.get_nodes_in_state_at_time(min_date.strftime("%Y-%m-%d"), SIModel.INFECTED)) + len(cascade.get_nodes_in_state_at_time(min_date.strftime("%Y-%m-%d"), SIModel.SUSCEPTIBLE))}")
    nodes_count_label.grid(row=0, column=0)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    total_infection_label = tk.Label(root, text=f"Total Infection Events: {len(cascade.get_infection_events())}")
    total_infection_label.pack(padx=10, pady=10)


    slider = ttk.Scale(button_frame, from_=0, to=(max_date - min_date).days, orient="horizontal", command=slider_changed, length=600)
    slider.pack(side=tk.LEFT)

    label_error = tk.Label(root, text="", fg="red")
    label_error.pack()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("CSV File Explorer")
    root.wm_state('zoomed')  # Maximize the window

    criteria_label = tk.Label(root, text="Infection Criteria:")
    criteria_label.pack(padx=10, pady=10, side='left')

    criteria_entry = tk.Entry(root)
    criteria_entry.pack(padx=10, pady=10,side='left')

    nodes_label = tk.Label(root, text="Number of Nodes:")
    nodes_label.pack(padx=10, pady=10, side='left')

    nodes_entry = tk.Entry(root)
    nodes_entry.pack(padx=10, pady=10, side='left')

    button = tk.Button(root, text="Open CSV File", command=lambda: open_file(root))
    button.pack(padx=10, pady=10, side='left')

    close_button = tk.Button(root, text="Close", command=root.quit)
    close_button.place(relx=1.0, rely=0.0, anchor="ne")  # Position in the top-right corner


    root.mainloop()
