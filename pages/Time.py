import os

from azure.cosmos import CosmosClient, exceptions, PartitionKey

import json
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

#set page title
#st.set_page_config(page_title="Time Analysis", page_icon="⏰", layout='wide')

st.title("⏰ Time Analysis")
st.sidebar.subheader('This section contains: \n 1) Definition Contributions per Year \n 2) Definition Contribution per Month \n 3) Definition Contributions per Day of Week \n 4) Definition Contributions per Hour ' )

from Homepage import share_df

# copy_dataframe
time_df = share_df.copy()

st.info('This section performs a chronogical analysis of the definitions given within the dictionary. It is separated by time measurements associated with each definiton along with a data visualization.')

# Create a dropdown to select the time measurement
time_unit = st.selectbox('Select time unit', ['Year', 'Month', 'Day of Week', 'Hour'])

# group the data based on the selected time unit and sum the word counts
# displays the data accordingly to the specified plot 
if time_unit == 'Year':
    grouped_data = time_df.groupby(time_df['time-entered'].dt.year).size()
elif time_unit == 'Month':
    grouped_data = time_df.groupby(time_df['time-entered'].dt.strftime('%B')).size()

elif time_unit == 'Day of Week':
    grouped_data = time_df.groupby(time_df['time-entered'].dt.strftime('%A')).size()
else:
    grouped_data = time_df.groupby(time_df['time-entered'].dt.hour).size()
    
chart_type = st.selectbox('Select chart type', ['Bar Chart', 'Line Chart'])
if chart_type == 'Bar Chart':
    st.bar_chart(grouped_data)
elif chart_type == 'Line Chart':
    st.line_chart(grouped_data)



