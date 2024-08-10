# Life Metric Tracker Project (TalagaLog)

## Overview

This ongoing project started as a health tracking application, initially developed as a final project for Data Structures at CU Boulder but has developed to allow for the tracking of any metrics. The aim of this tool is to track various health and other metrics over time, including sleep, weight, subjective wellbeing, exercise statistics, and more. The core data structure utilized in this project is a **Linked List Stack** implemented inside a **dictionary**, where each key stores a Linked List of a different metric. This structure efficiently manages health data, allowing users to add, remove, visualize, and analyze their personal health/other metrics. This data is then written to CSV files for long term data storage beyond the program's runtime. Python was chosen to practice object oriented programming in Python as opposed to C++. There is also a focus on visualizing and analyzing data to tie in and practice concepts/tools gained from a concurrent Data Science course. This project is not completed and will continue to see revisions and iterations over time, being used as a tool for practicing new techniques and tools. This is an application that I will begin using in my daily life to find potentially optimizations and changes that would better the user experience.

## Key Features

- **Linked List Stack for Data Storage and Management**: 
  - Each health metric is stored as a "LinkedListStack" in a dictionary, where each key describes a different metric. This stack structure allows for efficient addition of new data (pushed onto the top of the stack) and retrieval of the most recent entries.
  
- **Customizable Metrics**:
  - Users can add new health metrics to track, allowing for flexibility in what data the users can monitor.
  
- **CSV Storage**:
  - Data can be saved to and loaded from CSV files, where each metric’s data is stored as a list of tuples (date, value). This makes it easy to manage the data over time and is intuitive enough to allow users to go into the CSV file to make changes if necessary.
  
- **Data Visualization**:
  - The project includes tools for visualizing metrics over time using Matplotlib. This allows users to generate time-series plots and monitor progress over time
  
- **Correlation Analysis**:
  - Users can analyze the correlation between two different metrics, providing them with insights into how different aspects of their life are related (e.g, sleep quality and daily mood, or calories and weight)

## Data Structure Overview

### Linked List Stack

This structure stores individual metric data:

- **class StackNode**: 
  - Describes a single node in the linked list stack where every node contains data as a tuple (date and metric value) and a reference to the next node in the linked list stack.

- **class LinkedListStack**:
  - Implements a stack ADT using linked list nodes. Standard stack methods such as `push` (add data), `pop` (remove data), `peek` (view top of stack), `is_empty` (check if stack is empty), and `to_list` (convert stack to a Python list) are implemented.

### Dictionary of Linked List Stacks

- **class HealthTrackerDict**:
  - Stores multiple health metrics, with data stored as a linked list stack within a dictionary. Metric name is used as the dictionary key, and a linked list stack holds the metric data as a corresponding value

## User Commands

Once the program is running, users can interact through the following options:

1. **Load Data from CSV**: Loads existing data from a CSV file.
    - This should be done before visualization or analysis of data

2. **Save Data to CSV**: Saves the current new data to a CSV file.
    - This should be done after adding data, if no mistakes were made

3. **Add a New Metric**: Creates a new metric the user can start tracking.

4. **Add Data to an Existing Metric**: Adds a new data entry to an existing metric.

5. **View Available Metrics**: Lists all the metrics the user is currently tracking.

6. **Visualize Data**: Generates a time-series plot for a chosen metric.

7. **Analyze Correlation Between Metrics**: Calculates and displays correlation between two different health metrics on a scatter plot.

8. **Quit**: Exits the application.

## Sample Data

A sample.csv file is provided for demonstration/testing purposes. To use this data, enter "sample" as your name.