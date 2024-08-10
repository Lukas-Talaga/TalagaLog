import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import ast
import matplotlib.dates as mdates

# Define node class for LinkedListStack that will store health data
class StackNode:
    def __init__(self, data, next_node=None): # Next is None if this is the last node in the list
        self.data = data  # Stores data the user enters
        self.next = next_node  # Points to the next node in the LinkedListStack

# LinkedListStack class to store user data for one health metric
class LinkedListStack:
    def __init__(self):
        self.head = None  # Initialize head of list to None before data is added
    
    # Adds new data to head of list like a stack ADT
    def push(self, data):
        new_node = StackNode(data)  # Create a new node with the user's input data
        new_node.next = self.head  # Point new node to current head
        self.head = new_node  # Update head to be new node
    
    # Remove and return user data from the front of the list
    def pop(self):
        if self.head is None:  # Return None if list is empty
            return None
        ret_data = self.head.data  # Get data from front of the list
        self.head = self.head.next  # Change head to be the next node
        return ret_data  # Return data that was on top of the LinkedListStack
    
    # Not used for this implementation but is a common stack method
    def peek(self):
        if self.head is None:  # Return None if list is empty
            return None
        return self.head.data  # Return data at front of the list without removing
    
    # Check if list is empty
    def is_empty(self):
        empty = self.head is None # Check for presence of a head node
        return empty # Return True if there are no nodes in list
    
    # Convert LinkedListStack to built-in Python list to make some calculations easier
    def to_list(self):
        current_node = self.head  # Start at head of the list
        metric_data = []
        while current_node != None:
            metric_data.append(current_node.data)  # Add each node's data to the list
            current_node = current_node.next  # Move to the next node
        return metric_data

# Dictionary to store LinkedListStacks of different metrics
class HealthTrackerDict:
    def __init__(self, username):
        self.username = username  # Save user's name
        self.metrics = {}  # Each metric in dictionary is a linked list
    
    # Load data from .csv file into dictionary
    def load_data(self, csv_name):
        user_data_df = pd.read_csv(csv_name)  # Create Pandas DataFrame from .csv data
        for metric in user_data_df.columns: # Loop over columns where each is a different metric
            self.metrics[metric] = LinkedListStack()  # Create new LinkedListStack for each metric
            for data_value in reversed(user_data_df[metric].dropna().tolist()): # Store data in chronological order to make adding new data easier
                self.metrics[metric].push(data_value)  # Add each piece of data to head of the LinkedListStack
    
    # Save dictionary of LinkedListStacks to .csv
    def save_data(self):
        metrics = self.metrics.items() # Store name of metric and LinkedListStack as pairs
        data = {metric: user_data.to_list() for metric, user_data in metrics} # Dictionary comprehension to store each metric as a Python list
        max_length = max(len(lst) for lst in data.values()) # Find max list length
        for metric in data:
            if len(data[metric]) < max_length:
                data[metric] += [None] * (max_length - len(data[metric])) # Pandas needs all lists to be the same length
        user_data_df = pd.DataFrame(data)  # Convert data to Pandas DataFrame
        user_data_df.to_csv(self.username+".csv", index=False)  # Use Pandas to save DataFrame to .csv file
    
    # Add new metric (e.g. "weight", "sleep", "exercise_name") to start tracking
    def add_metric(self, new_metric_name):
        if new_metric_name not in self.metrics:
            self.metrics[new_metric_name] = LinkedListStack()  # Create new LinkedListStack for new metric
    
    # Add new data to specific metric with date for time-series visualization
    def add_data(self, new_metric_name, user_data, date=None):
        if new_metric_name in self.metrics:
            if date is None: # Handle not inserting a date (makes tracking easier and faster)
                date = datetime.now().strftime('%Y-%m-%d')  # Use current date if none provided (convert datetime object to year-month-day string like user inputs)
            self.metrics[new_metric_name].push((date, user_data))  # Store new user data as a tuple with date
        else:
            print(f"Metric {new_metric_name} does not exist.")
    
    # Check to see what metrics are available to add to
    def view_metrics(self):
        return list(self.metrics.keys()) # Return keys of corresponding to each LinkedListStack
    
    # Get data for a specific metric
    def get_data(self, metric_name):
        if metric_name in self.metrics:
            return self.metrics[metric_name].to_list() # Convert data to list and return for printing
        else:
            print(f"Metric {metric_name} does not exist.") # Tell user if metric does not exist
            return None
    
    # Visualize data for a specific metric as time-series
    def visualize_data(self, metric_name):
        if metric_name in self.metrics:
            data = self.metrics[metric_name].to_list() # Store data as Python list for plotting
            data = [ast.literal_eval(tuple) for tuple in data] # Convert strings to Python literals
            dates = [datetime.strptime(day, '%Y-%m-%d') for day, user_data in data] # Convert dates to datetime objects with list comprehension and store in variable
            values = [int(user_data) for day, user_data in data] # Pull out user data from tuples and store in variable
            plt.figure(figsize=(10, 5)) # Choose figure size
            plt.plot(dates, values, marker='o') # Plot data as circles
            plt.title(f"{metric_name} Over Time") 
            plt.xlabel("Date")
            plt.ylabel(metric_name)
            plt.xticks(rotation=45) # Rotate dates to save space
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d')) # Change from plotting datetime to just date, no time
            plt.gca().xaxis.set_major_locator(mdates.DayLocator()) # Make sure each day is only plotted once
            plt.tight_layout()
            plt.show()
        else:
            print(f"Metric {metric_name} does not exist.") # Tell user if metric does not exist

    # Analyze correlation between two metrics, handling different lengths of data
    def analyze_correlation(self, metric1, metric2):
        if metric1 in self.metrics and metric2 in self.metrics:
            # Convert linked lists to Python lists of literals
            data_metric1 = self.metrics[metric1].to_list()
            data_metric1 = [ast.literal_eval(tuple) for tuple in data_metric1]
            data_metric2 = self.metrics[metric2].to_list()
            data_metric2 = [ast.literal_eval(tuple) for tuple in data_metric2]
            # Create dictionaries from lists to match up dates
            dict_metric1 = {date: value for date, value in data_metric1}
            dict_metric2 = {date: value for date, value in data_metric2}
            # Create sets to store dates for each metric
            set_dates_metric1 = set(dict_metric1.keys())
            set_dates_metric2 = set(dict_metric2.keys())
            common_dates = set_dates_metric1.intersection(set_dates_metric2) # Store intersection of data between two metrics based on date
            if common_dates:
                # Extract data for common dates between metrics
                values_metric1 = [float(dict_metric1[date]) for date in common_dates if dict_metric1[date] is not None]
                values_metric2 = [float(dict_metric2[date]) for date in common_dates if dict_metric2[date] is not None]
                corr = np.corrcoef(values_metric1, values_metric2)[0, 1] # Calculate correlation coefficient with NumPy
                plt.figure(figsize=(10, 5))  # Choose figure size
                plt.scatter(values_metric1, values_metric2)  # Plot data as scatterplot
                plt.title(f"Correlation between {metric1} and {metric2}: {corr:.2f}")  # Round correlation and title plot
                plt.xlabel(metric1)
                plt.ylabel(metric2)
                plt.show()
            else:
                print(f"No common dates between {metric1} and {metric2}.")
        else:
            print(f"One or both metrics do not exist.")


# Define user interaction with health tracker
def main():
    username = input("\nEnter your name: ")
    tracker = HealthTrackerDict(username)

    while True: # Loop until user quits
        print("\n*Please only enter numbers or dates*")
        print("\nOptions:")
        print("1. Load data from CSV file")
        print("2. Save data to CSV file")
        print("3. Add a new metric to track")
        print("4. Add data to an existing metric")
        print("5. View available metrics")
        print("6. Visualize data")
        print("7. Analyze correlation between metrics")
        print("8. Quit\n")

        choice = input("Enter your choice: ") # Store the user's choice

        # Find user's choice and enter condition
        if choice == "1":
            file_name = tracker.username + ".csv"
            tracker.load_data(file_name)
            print(f"Data loaded from {tracker.username}.csv")
        elif choice == "2":
            tracker.save_data()
            print(f"Data saved as {tracker.username}.csv")
        elif choice == "3":
            metric_name = input("Enter the name of a new metric: ")
            tracker.add_metric(metric_name)
        elif choice == "4":
            metric_name = input("Enter the metric name: ")
            data = input(f"Enter the data for {metric_name}: ")
            date = input("Enter the date (YYYY-MM-DD) or leave blank for today's date: ")
            tracker.add_data(metric_name, data, date if date != "" else None)
        elif choice == "5":
            print("Available metrics:", tracker.view_metrics())
        elif choice == "6":
            metric_name = input("Enter the metric name to visualize: ")
            tracker.visualize_data(metric_name)
        elif choice == "7":
            metric1 = input("Enter the first metric: ")
            metric2 = input("Enter the second metric: ")
            tracker.analyze_correlation(metric1, metric2)
        elif choice == "8":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
