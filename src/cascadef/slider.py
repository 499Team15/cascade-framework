import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk
from datetime import datetime, timedelta

def open_file():
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filename:
        df = pd.read_csv(filename)
        # Convert 'created_at' column to datetime
        df['created_at'] = pd.to_datetime(df['created_at'])
        min_date = df['created_at'].min()
        max_date = df['created_at'].max()
        create_slider(min_date, max_date)

def create_slider(min_date, max_date):
    root = tk.Toplevel()
    root.title("Date Selector")
    root.geometry("800x800")

    label = tk.Label(root, text="")
    label.pack(padx=10, pady=10)

    def get_selected_date(value):
        selected_date = min_date + timedelta(days=value)
        label.config(text="Selected date: " + selected_date.strftime("%Y-%m-%d"))
        date_entry.delete(0, tk.END)
        date_entry.insert(0, selected_date.strftime("%Y-%m-%d"))

    def slider_changed(event):
        value = int(slider.get())
        get_selected_date(value)

    def manual_date_change(event=None):
        try:
            input_date = pd.to_datetime(date_entry.get())
            if min_date <= input_date <= max_date:
                days_diff = (input_date - min_date).days
                slider.set(days_diff)
                label.config(text="Selected date: " + input_date.strftime("%Y-%m-%d"))
            else:
                raise ValueError
        except ValueError:
            label.config(text="Invalid date! Please enter a date within the range.")

    date_frame = tk.Frame(root)
    date_frame.pack(padx=10, pady=10)

    date_label = tk.Label(date_frame, text="Selected Date:")
    date_label.grid(row=0, column=0)

    date_entry = tk.Entry(date_frame)
    date_entry.grid(row=0, column=1)
    date_entry.bind("<Return>", manual_date_change)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    slider = ttk.Scale(button_frame, from_=0, to=(max_date - min_date).days, orient="horizontal", command=slider_changed, length=600)
    slider.pack(side=tk.LEFT)

    select_button = tk.Button(button_frame, text="Select Date", command=manual_date_change)
    select_button.pack(side=tk.LEFT)

    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("CSV File Explorer")
    root.geometry("800x800")

    button = tk.Button(root, text="Open CSV File", command=open_file)
    button.pack(padx=10, pady=10)

    root.mainloop()
import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk
from datetime import datetime, timedelta

def open_file():
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filename:
        df = pd.read_csv(filename)
        # Convert 'created_at' column to datetime
        df['created_at'] = pd.to_datetime(df['created_at'])
        min_date = df['created_at'].min()
        max_date = df['created_at'].max()
        create_slider(min_date, max_date)

def create_slider(min_date, max_date):
    root = tk.Toplevel()
    root.title("Date Selector")
    root.geometry("800x800")

    label = tk.Label(root, text="")
    label.pack(padx=10, pady=10)

    def get_selected_date(value):
        selected_date = min_date + timedelta(days=value)
        label.config(text="Selected date: " + selected_date.strftime("%Y-%m-%d"))
        date_entry.delete(0, tk.END)
        date_entry.insert(0, selected_date.strftime("%Y-%m-%d"))

    def slider_changed(event):
        value = int(slider.get())
        get_selected_date(value)

    def manual_date_change(event=None):
        try:
            input_date = pd.to_datetime(date_entry.get())
            if min_date <= input_date <= max_date:
                days_diff = (input_date - min_date).days
                slider.set(days_diff)
                label.config(text="Selected date: " + input_date.strftime("%Y-%m-%d"))
            else:
                raise ValueError
        except ValueError:
            label.config(text="Invalid date! Please enter a date within the range.")

    date_frame = tk.Frame(root)
    date_frame.pack(padx=10, pady=10)

    date_label = tk.Label(date_frame, text="Selected Date:")
    date_label.grid(row=0, column=0)

    date_entry = tk.Entry(date_frame)
    date_entry.grid(row=0, column=1)
    date_entry.bind("<Return>", manual_date_change)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    slider = ttk.Scale(button_frame, from_=0, to=(max_date - min_date).days, orient="horizontal", command=slider_changed, length=600)
    slider.pack(side=tk.LEFT)

    select_button = tk.Button(button_frame, text="Select Date", command=manual_date_change)
    select_button.pack(side=tk.LEFT)

    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("CSV File Explorer")
    root.geometry("800x800")

    button = tk.Button(root, text="Open CSV File", command=open_file)
    button.pack(padx=10, pady=10)

    root.mainloop()
