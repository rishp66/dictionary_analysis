import os

from azure.cosmos import CosmosClient, exceptions, PartitionKey

import json
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from textblob import TextBlob

from Homepage import share_df

# copy_dataframe
imported_df = share_df.copy()
# set page title
#st.set_page_config(page_title="Author Analysis", page_icon="🖋️", layout='wide')

st.title("🖋️ Author Analysis")
st.sidebar.subheader('This section contains: \n 1) Frequency of contribution \n 2) Sentiment analysis per author')

# info
st.info('This section performs a sentiment analysis of the authors for their contributions in the dictionary.')

# intro p2
st.write('Below is the total contributions per individual author.')

defs_by_author = pd.DataFrame(imported_df['author'].value_counts().reset_index())
defs_by_author.columns = ['author', 'count']

# Create a vertical bar plot
fig = px.bar(defs_by_author, x='author', y='count',
             title='Count Contributions per Author')

# Display the plot in Streamlit
st.plotly_chart(fig, use_container_width=True)

pd.set_option("display.max_colwidth", None)

# Create a new DataFrame with 'author' and 'word' columns
df_main = imported_df[['author', 'word', 'content']].reset_index(drop=True)

# Rename the columns to 'Authors' and 'Word' and 'Definitions'
df_main = df_main.rename(columns={'author': 'Authors', 'word': 'Word', 'content': 'Definition'})


st.subheader('DataFrame Example View')
st.info("Below is an example of what a fraction of the Authors dataframe looks like.")


# give an example view of the dataframe that changes everytime
rands = np.random.randint(0, len(df_main), 5)
st.dataframe(df_main.iloc[rands], hide_index=True)

# now performing sentiment analysis

# Perform sentiment analysis on the 'Definition' column

def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

df_main['sentiment_polarity'], df_main['sentiment_subjectivity'] = zip(*df_main['Definition'].apply(get_sentiment))

# Grouping by polarity
sentiment_by_p_author = df_main.groupby('Authors')[['sentiment_polarity']].mean()
sentiment_by_p_author = sentiment_by_p_author.sort_values(by='sentiment_polarity', ascending=True).reset_index()

# Grouping by subjectivity
sentiment_by_s_author = df_main.groupby('Authors')[['sentiment_subjectivity']].mean()
sentiment_by_s_author = sentiment_by_s_author.sort_values(by='sentiment_subjectivity', ascending=True).reset_index()

# Grouping by overall sentiment
df_main['overall_sentiment'] = (df_main['sentiment_polarity'] + df_main['sentiment_subjectivity']) / 2.0
sentiment_by_o_author = df_main.groupby('Authors')['overall_sentiment'].mean()
sentiment_by_o_author = sentiment_by_o_author.sort_values(ascending=True).reset_index()

st.info('We will now visualize the Authors Data using Plotly!', icon="📊")

# Create a dropdown menu for selecting the graph
selected_graph = st.selectbox("**Select Graph**", ["Sentiment Polarity", "Sentiment Subjectivity", "Overall Sentiment"])

# Utilize Plotly for horizontal barcharts side by side
fig = make_subplots(rows=1, cols=1, subplot_titles=[selected_graph])

# Function to add trace based on the selected graph
def add_trace_for_graph(selected_graph, color_scale):
    if selected_graph == "Sentiment Polarity":
        sentiment_data = sentiment_by_p_author
    elif selected_graph == "Sentiment Subjectivity":
        sentiment_data = sentiment_by_s_author
    elif selected_graph == "Overall Sentiment":
        sentiment_data = sentiment_by_o_author
    
    return go.Bar(
        x=sentiment_data[selected_graph.lower().replace(" ", "_")],
        y=sentiment_data['Authors'],
        orientation='h',
        marker=dict(color=sentiment_data[selected_graph.lower().replace(" ", "_")], colorscale=color_scale),
        name=selected_graph
    )

# Plot the selected graph
fig.add_trace(add_trace_for_graph(selected_graph, px.colors.sequential.Agsunset))

# Add a solid line at x=0 for all plots
fig.add_shape(
    type="line",
    x0=0, x1=0,
    y0=0, y1=len(sentiment_by_p_author),
    line=dict(color="white", width=2)
)

# Set layout properties
fig.update_layout(
    title_text=f"{selected_graph} Analysis per Author",
    title_x=0.5,
    height=1000,
    yaxis=dict(tickmode='linear')
)

# Display the Plotly chart in Streamlit
st.plotly_chart(fig, use_container_width=True)






