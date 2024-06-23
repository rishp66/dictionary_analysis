import os

from azure.cosmos import CosmosClient

import pandas as pd
import pickle
import numpy as np
import streamlit as st
import os
from dotenv import load_dotenv

from textblob import TextBlob

# titling page
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    layout='wide'
)

# show sidebar

# Creating Access Controls using Streamlit secrets
load_dotenv()
uri = os.getenv('uri')
key = os.getenv('key')
client = CosmosClient(url=uri, credential=key)

database = client.get_database_client("clouddictionary")

container = database.get_container_client("definitions")


query = 'SELECT * FROM c'
items = container.query_items(query, enable_cross_partition_query=True)

df = pd.DataFrame()

# Iterate over the list of items
for item in items:
    item_df = pd.json_normalize(item)  # Use pd.json_normalize() to flatten nested JSON structures
    df = pd.concat([df, item_df], ignore_index=True)



# Remove unnecessary rows from the DataFrame
df = df.drop(columns=['id', '_rid', '_self', '_attachments', '_etag','author.link'], errors='ignore')

# Changing Timestamp column from Unix time stamp to UTC time
df['_ts'] = pd.to_datetime(df['_ts'], unit='s', utc=True)

df.rename(columns={'_ts': 'time-entered', 'author.name': 'author', 'learnMoreUrl': 'url'}, inplace=True)

# sharing dataframe
share_df = df.copy()

# Creating Introduction to Page
with st.container():
    st.title("☁️ Cloud Dictionary Analysis 📊")
    st.markdown('This data analysis was performed using the [DefineTheCloud](https://definethecloud.guide) Azure CosmosDB data to perform an analysis of definitons provided, the authors who provided them, and the timing of both.')
    code = '''def my_tech_used():
    - Azure CosmosDB NoSQL Data
    - Python: numpy, pandas, seaborn'''
    st.caption('By: Rish Pednekar')
    st.code(code, language='python')

# View the info of the database
with st.container():
    df_key_vals = pd.DataFrame(df.columns)
    df_key_vals['Description'] = np.nan
    df_key_vals.rename(columns={0: 'Value'}, inplace=True)

# providing description to columns
with st.container():
    st.divider()
    st.subheader("Data Description")
    list_defs = ['This is the technical term provided by the contributor.', 
                'Definition of the technical term',
                'URL link to the source of the definition',
                'Genre of technical term within DefineTheCloud',
                'Shorthand for the tag',
                'Time when word was submitted by the contributor',
                'Identity of contributor']

    df_key_vals['Description'] = list_defs

    st.table(df_key_vals)


st.subheader('DataFrame Example View')
st.caption("Below is an example of what a fraction of the dataframe looks like.")

# give an example view of the dataframe that changes everytime
rands = np.random.randint(0, len(df), 5)
st.dataframe(df.iloc[rands], hide_index=True)

st.divider()

st.info('See the other pages for the in-depth analysis!')



