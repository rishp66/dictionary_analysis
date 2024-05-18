
import os

from azure.cosmos import CosmosClient, exceptions, PartitionKey

import json
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import random

from textblob import TextBlob

from Homepage import share_df

#set page title
# titling page
st.set_page_config(
    layout='wide',
    page_icon="📖",
    page_title="Dictionary Analysis",
    initial_sidebar_state='expanded'
)

st.title("📖 Dictionary Analysis")
st.sidebar.subheader('This section contains: \n - Sentiment analysis of the content or definitions within the DefineTheCloud. \n - It wll also be separated by tag of the category of the word.')


st.info('This section performs a sentiment analysis of the definitions given within the dictionary. It is also separated by the tag associated with each definiton along with a data visualization.')

# creating the imported dataframe
imported_df = share_df.copy()

st.write('Below is a diagram showing all tags and how many words belong in each tag.')



# generate a count plot using plotly
fig = px.bar(imported_df['tag'].value_counts().reset_index(), x='tag', y='count',
                 title='Count Definitions by Tag')
st.plotly_chart(fig, use_container_width= True)

st.divider()

st.header("Sentiment Analysis")
st.info("Below, I have shown the content of each definition, the tag of the definition, and the sentiment analysis calculation of the definition.")

# defining sentiment analyzer method using TextBlob
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_polarity = blob.sentiment.polarity
    sentiment_subjectivity = blob.sentiment.subjectivity
    return sentiment_polarity, sentiment_subjectivity


# get overall sentiment of the database definitions
sentiment_data = pd.DataFrame()
sentiment_data['content'] = imported_df['content'].copy()
sentiment_data['tag'] = imported_df['tag'].copy()
sentiment_data[['sentiment_polarity', 'sentiment_subjectivity']] = sentiment_data['content'].apply(analyze_sentiment).apply(pd.Series)

st.info('We denote anything below 0 as being negative, 0 as neutral, and above 0 as positive.')
st.dataframe(sentiment_data, use_container_width=True)

st.caption('''### Sentiment Analysis in NLP Explanation --

Sentiment analysis involves assessing the sentiment of a text — whether it is positive, negative, or neutral. This analysis is crucial for understanding opinions and emotions expressed in various contexts.

- **Polarity:** Measures the positivity or negativity of the text.
- **Subjectivity:** Determines the objectivity or subjectivity of the text.

### Techniques:
1. **Rule-based Methods:** Define rules to identify positive and negative words.
2. **Machine Learning & Deep Learning:** Trained on labeled datasets to identify sentiment patterns.

Subjectivity analysis is essential for distinguishing between factual information and personal opinions in texts.

For more details, check the [source article](https://iq.opengenus.org/polarity-and-subjectivity-in-nlp/).
''')


# get dataframe containing the average sentiment score per tag
st.divider()
st.header('Sentiment per Tag')
st.caption('Below shows the following command to group and aggregate each tag for their own sentiment scores.')
st.code('''
        
        sentiment_by_p_tag = sentiment_data.groupby('tag')[['sentiment_polarity']].mean()
        sentiment_by_s_tag = sentiment_data.groupby('tag')[['sentiment_subjectivity']].mean()
        sentiment_data['overall_sentiment'] = (sentiment_data['sentiment_polarity'] + sentiment_data['sentiment_subjectivity']) / 2.0
        sentiment_by_o_tag = sentiment_data.groupby('tag')['overall_sentiment'].mean()
        ''')

# grouping by polarity
sentiment_by_p_tag = sentiment_data.groupby('tag')[['sentiment_polarity']].mean()
sentiment_by_p_tag = sentiment_by_p_tag.sort_values(by='sentiment_polarity', ascending=True).reset_index()

# grouping by subjectivity
sentiment_by_s_tag = sentiment_data.groupby('tag')[['sentiment_subjectivity']].mean()
sentiment_by_s_tag = sentiment_by_s_tag.sort_values(by='sentiment_subjectivity', ascending=True).reset_index()

# group by overall
# Group by overall sentiment
sentiment_data['overall_sentiment'] = (sentiment_data['sentiment_polarity'] + sentiment_data['sentiment_subjectivity']) / 2.0
sentiment_by_o_tag = sentiment_data.groupby('tag')['overall_sentiment'].mean()
sentiment_by_o_tag = sentiment_by_o_tag.sort_values(ascending=True).reset_index()


st.info('We will now visualize the data using Plotly!', icon="📊")

# Create a dropdown menu for selecting the graph
selected_graph = st.selectbox("**Select Graph**", ["Sentiment Polarity", "Sentiment Subjectivity", "Overall Sentiment"])

# Utilize Plotly for horizontal barcharts side by side
fig = make_subplots(rows=1, cols=1, subplot_titles=[selected_graph])

# Function to add trace based on the selected graph
def add_trace_for_graph(selected_graph, color_scale):
    if selected_graph == "Sentiment Polarity":
        sentiment_data = sentiment_by_p_tag
    elif selected_graph == "Sentiment Subjectivity":
        sentiment_data = sentiment_by_s_tag
    elif selected_graph == "Overall Sentiment":
        sentiment_data = sentiment_by_o_tag

    return go.Bar(
        x=sentiment_data[selected_graph.lower().replace(" ", "_")],
        y=sentiment_data['tag'],
        orientation='h',
        marker=dict(color=sentiment_data[selected_graph.lower().replace(" ", "_")], colorscale=color_scale),
        name=selected_graph
    )

# Plot the selected graph
fig.add_trace(add_trace_for_graph(selected_graph, px.colors.sequential.Agsunset))

# Add a solid line at x=0 for all plots
fig.add_shape(
    type="line",
    x0=0,
    x1=0,
    y0=0,
    y1=len(sentiment_by_p_tag),
    line=dict(color="white", width=2)
)

# Set layout properties
fig.update_layout(
    title_text=f"{selected_graph} Analysis per Tag",
    title_x=0.5,
    height=600
)

# Display the Plotly chart in Streamlit
st.plotly_chart(fig, use_container_width=True)


