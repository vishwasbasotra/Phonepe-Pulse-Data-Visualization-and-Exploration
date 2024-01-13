# Phonepe Pulse Data Visualization

## Introduction 

* PhonePe has become one of the most popular digital payment platforms in India, with millions of users relying on it for their day-to-day transactions. The app is known for its simplicity, user-friendly interface, and fast and secure payment processing. It has also won several awards and accolades for its innovative features and contributions to the digital payments industry.

* We create a web app to analyse the Phonepe transaction and users depending on various Years, Quarters, States, and Types of transaction and give a Geographical and Geo visualization output based on given requirements.

###### " Disclaimer:-This data between 2018 to 2022 in INDIA only "

![Intro GUI](https://github.com/vishwasbasotra/Phonepe-Pulse-Data-Visualization-and-Exploration/blob/main/demo.png)

## Developer Guide 

### 1. Tools install

* VS Code.
* Jupyter notebook.
* Python 3.11.0 or higher.
* MySQL
* Git

### 2. Requirement Libraries to Install

* pip install pandas numpy os json requests subprocess mysql.connector sqlalchemy pymysql streamlit plotly.express

### 3. Import Libraries

**clone libraries**
* import requests
* import subprocess

**pandas, numpy and file handling libraries**
* import pandas as pd
* import numpy as np
* import os
* import json

**SQL libraries**
* import mysql.connector
* import sqlalchemy
* from sqlalchemy import create_engine

**Dashboard libraries**
* import streamlit as st
* import plotly.express as px

### 4. E T L Process

#### a) Extract data

* Initially, we Clone the data from the Phonepe GitHub repository by using Python libraries. https://github.com/PhonePe/pulse.git

#### b) Process and Transform the data

* Process the clone data by using Python algorithms and transform the processed data into DataFrame formate.

#### c) Load  data 

* Finally, create a connection to the MySQL server and create a Database and stored the Transformed data in the MySQL server by using the given method. **df.to_sql('table_name', connection, if_exists = 'replace', index = False, dtype={'Col_name':sqlalchemy.types.datatype()})**

### 5. E D A Process and Frame work

#### a) Access MySQL DB 

* Create a connection to the MySQL server and access the specified MySQL DataBase by using pymysql library 

#### b) Filter the data

* Filter and process the collected data depending on the given requirements by using SQL queries

#### c) Visualization 

* Finally, create a Dashboard by using Streamlit and applying selection and dropdown options on the Dashboard and show the output are Geo visualization, bar chart, and Dataframe Table
