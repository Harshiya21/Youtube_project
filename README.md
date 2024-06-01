
YouTube Data Harvesting and Warehousing using SQL and Streamlit

    This project aims to develop a user-friendly Streamlit application leveraging the Google API to gather data from YouTube channels. The collected data is initially stored in a pandas DataFrame and subsequently migrated to a SQL data warehouse for further analysis and exploration. The entire process is made accessible and seamless through the Streamlit app interface.


Technologies Used

* Python scripting
* Data Collection
* Streamlit
* API integration
* Data Management using SQL 
Installation

* pip install google-api-python-client
* pip install pandas
* pip install mysql.connector
* pip install sqlalchemy
* pip install streamlit
* pip install iso8601

Features

* Retrieve data from the YouTube API, including channel information, playlists, videos, and comments.

* Store the retrieved data in a pandas database.

* Migrate the data to a MySQL data warehouse.

* Used SQL queries to join the tables in the SQL data warehouse and Used a Python SQL library such as SQLAlchemy to interact with the SQL database.

* Analyze and visualize data using Streamlit

* Perform queries on the MySQL data warehouse.

* Display all ten queries in a table format within the Streamlit application.

Retrieving data from YouTube API
     
    The project leverages the Google API to fetch extensive data from YouTube channels Containing details about channels, playlists, videos, and comments.
    
Storing data in Pandas Data Frame

    The collected data is stored in memory using a pandas DataFrame.

Migrating data to a MySQL data warehouse
     
    The application enables users to transfer data from a pandas DataFrame to a MySQL data warehouse, utilizing SQL libraries such as SQLAlchemy for interaction with the MySQL database. Users can input channel IDs to migrate data from the pandas DataFrame to the MySQL database. The data is then partitioned into distinct tables, including channels, videos, and comments, using MySQL queries to address all ten queries.
    
Analysis
      
    The Streamlit app features a user-friendly interface, facilitating interactive exploration and customization of visualizations and explore data interactively, aiding in the discovery of valuable insights and informed decision-making.
    
Conclusion

    In this project leverages the Google API to collect, store, and analyze data from YouTube channels, making it accessible through a user-friendly Streamlit application. 

Demo

    https://drive.google.com/file/d/1APAOtNTDb5l4yBjDAsoDDsoY5lMY1CxV/view?usp=sharing
    

