import pandas as pd
import json
import os
import streamlit as st
import sqlalchemy as sa
import mysql.connector
from mysql.connector import Error
from streamlit_option_menu import option_menu
from PIL import Image
import plotly.express as px

#Configuring streamlit header
im = Image.open("phonepe-logo.png")
st.set_page_config(page_title="PhonePe Pulse Data Visualization", page_icon=im, layout='wide')

# header section
st.title(":violet[PhonePe Pulse Data Visualization:]")

#col1,col2 = st.columns([0.45,0.55])
row_input = st.columns((1,0.5,0.5,0.5))
with row_input[0]:
    selected_option = st.selectbox(
                'Please select the channel data you want to migrate to MySQL:',('Transactional', 'User'),placeholder='Select',label_visibility='hidden')
with row_input[1]:
    selected_year = st.selectbox(
                'Year:',('2018', '2019','2020', '2021', '2022'),index=4,placeholder='Select')
with row_input[2]:
    selected_quater = st.selectbox(
                label='Quater:',index=3, options=('Q1', 'Q2','Q3', 'Q4'))

indian_states = json.load(open("states_india.geojson",'r'))

myslq_engine = mysql.connector.connect(user='root', 
                                       password='admin', 
                                       host='localhost', 
                                       port='3306', 
                                       database = 'phonepe')

crsr = myslq_engine.cursor()
        
# SQL query to be executed in the database
sql_command = """SELECT * from aggregate_transaction;
"""

# execute the statement
crsr.execute(sql_command)
queryResult = crsr.fetchall()

#adding result to the dataframe
i = [i for i in range(1, len(queryResult)+1)]
df = pd.DataFrame(queryResult, columns=['State', 
                                        'Year', 
                                        'Quater', 
                                        'Transaction_type', 
                                        'Transaction_count', 
                                        'Transaction_amount', 
                                        'ID',
                                        'Transaction_amountScale' 
                                        ], index=i)
myslq_engine.close()
    
fig = px.choropleth_mapbox(
                    df, 
                    locations = 'ID', 
                    geojson=indian_states, 
                    color='Transacion_amountScale',
                    hover_name = 'State',
                    hover_data=['Transacion_amount'],
                    mapbox_style='carto-positron',
                    center={'lat':24, 'lon':78},
                    zoom = 3)
st.plotly_chart(fig,use_container_width=True)