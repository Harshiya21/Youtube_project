
# Phonepe-Pulse-Data-Visualization-and-Exploration

DESCRIPTION


        PhonePe is a digital payments platform that enables users to make transactions, transfer money, pay bills, and recharge mobile phones through a mobile application.The PhonePe Pulse Data Visualization and Exploration project aims to gather valuable information from PhonePe's GitHub repository, process the data, and present it using an interactive dashboard that's visually appealing. This is accomplished using Python, Streamlit, and Plotly.
## About PhonePe-Pulse Data

   This data has been structured to provide details of following two sections with data cuts on Transactions
and Users of PhonePe Pulse - Explore tab.

1.Aggregated - Aggregated values of various payment    categories as shown under Categories sectio
2.Map - Total values at the State and District levels.
3.Top - Totals of top States / Districts /Pin Codes.
## Table of Contents
 
>Requirements
Installation
>Features

## Requirements

1.Python -- Python: Python is a widely-used programming language known for its simplicity and readability.


2.Plotly: Plotly is a Python module used for data visualization, offering support for various types of graphs and charts.

3.Pandas: Pandas is a Python library commonly used for data manipulation and analysis, providing powerful tools for working with structured data.

4.Streamlit: Streamlit is a Python framework designed for quickly building and sharing interactive web applications for machine learning and data science projects.

5.GitPython (git.repo.base): GitPython is a Python library that facilitates interaction with Git repositories, including functionalities like cloning repositories and managing local copies of data.

6.mysql.connector: The mysql.connector library enables Python programs to connect to MySQL databases, allowing for data retrieval, manipulation, and storage within Python applications.

7.JSON: The JSON library in Python provides functions for parsing JSON data into Python dictionaries or lists, enabling easy handling of JSON-formatted data within Python scripts.

8.os: The os module in Python provides functions for interacting with the operating system, allowing for tasks such as file manipulation, directory operations, and environment variable access within Python programs.
## Installation

To run this project, you need to install the following packages:

import git
repository_url = "https://github.com/PhonePe/pulse.git"

 pip install pandas
 pip install mysql-connector-python
 pip install requests
 pip install matplotlib
 pip install plotly
 pip install streamlit
## Features

    Data Collection: Easily clone PhonePe Pulse data from GitHub to your local directory, ensuring seamless access for analysis.

    Data Overview: Dive deep into your data with detailed breakdowns by states, years, quarters, and more, empowering informed decision-making.

    Migrating Data to SQL Database: Simplify your workflow by converting PhonePe Pulse data to a MYSQL Database, ensuring efficient querying and analysis.

    Interactive Streamlit Interface: Explore dynamic charts and apply filters effortlessly with our intuitive Streamlit app, enhancing data-driven decisions.

    Dynamic Visualizations with Plotly: Unlock insights with a variety of dynamic charts, from line charts to scatter plots, enhancing data exploration.

    Data Insights and Exploration: Navigate through nuanced insights across various metrics, uncovering patterns and trends for informed decision-making.

    Live Geo Visualization Dashboard: Interact with live maps to gain real-time insights and unlock the full potential of geographical data.

    Top Performers Highlight: Easily identify top states, districts, and pincodes through user-friendly visualizations, empowering focused decision-making.

    Data-Driven Decision Making: Leverage insights from PhonePe Pulse data to drive informed and impactful decisions, ensuring precision and confidence.
## Project Workflow

Step 1: Installing and Importing Required Libraries

    First, make sure you have all the needed libraries installed by using pip install followed by the name of each library. This ensures that your Python environment has access to the tools you'll be using.

    Once installed, import these libraries into your program using the import statement. This step makes the library's functions and features available for use within your code.

>import streamlit as st
import pandas as pd 
>import mysql.connector
import matplotlib.pyplot as plt 
>import plotly.express as px 
import requests 
>import json 

Step 2: Data Extraction - Cloning the GitHub Repository

    To fetch the data from the PhonePe Pulse GitHub repository, you'll need to clone the repository onto your local machine.

    First, ensure that Git is installed on your computer. You can download and install Git from the official website, "https://www.git-scm.com/downloads".

    After downloading and installing Git, verify its installation by opening a command prompt and typing git. You should see messages indicating that Git Bash is successfully installed.

    Next, set up Git by providing your username and email for accessing Git repositories.

    Now, create a new folder where you want to store the cloned repository.

    Open your terminal in Visual Studio Code or any other code editor and navigate to the newly created folder.

    In the terminal, type the command git clone https://github.com/PhonePe/pulse.git and press Enter. This command clones the PhonePe Pulse repository into your local folder.

    Once the cloning process is complete, check the folder to ensure that the data has been successfully cloned from the repository.

Step 3 -- Data Tranformation - JSON to Pandas DataFrame

Note : This step is performed in the .ipynb Python notebook that is in a Jupyter Notebook, because it is comparitively easy to visualize. You can check the ipynb notebook attached above for the code implementation of the process below.


    After extracting data from the PhonePe Pulse Repository, which is in JSON format, the next step is to transform this data into a format that's easier to work with. We'll use Pandas, a Python library, to convert the JSON data into a Pandas DataFrame.

    This transformation allows us to efficiently visualize the data as tables and perform tasks like data cleaning to handle any missing values. Additionally, it enables us to create visualizations, such as graphs, using the Plotly module.

    To achieve this, we'll iterate through each JSON file in each folder using a for loop. Within this loop, we'll use the os and json packages to access and read each JSON file. Then, we'll extract the necessary key-value pairs and combine them into a DataFrame using Pandas.

    This process simplifies the data, making it easier to analyze and visualize for further insights.

Step 4 -- Data Insertion - Inserting the Data into MySQL Database

Note : You can check the .py notebook attched above for the code implementation of the below process.

    After that one need to create a phpmyadmin Database in there local system. Now below is the Python code to connect to that SQL Database.

>mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="phonepae")
print(mydb)
>mycursor = mydb.cursor(buffered=True)
 
    After successfully establishing the connection, the next step involves creating the necessary tables in the MySQL database, each with the required columns. Once the tables are created, the data transformed in Step 3 needs to be inserted into these tables.

Step 5 -- To create a Streamlit Application

Note : You can check the .py file attched above for the code implementation of this streamlit Application.

    This project produces a dynamic dashboard using Streamlit, offering live geo visualizations and insights extracted from the PhonePe Pulse GitHub repository. Data is efficiently stored in a MySQL database for quick retrieval and the dashboard updates in real-time to reflect the latest information.

    Accessible through a web browser, users can navigate through interactive visualizations and explore various facts and figures seamlessly. This dashboard serves as a valuable resource for data analysis and informed decision-making.

    This user-friendly interface is powered by Streamlit, while Plotly's built-in functionalities handle the data visualization aspects.


## DEMO

    https://drive.google.com/file/d/1-Bb4wjx56vTApFQZNhXW88GCtyADZDgY/view?usp=sharing