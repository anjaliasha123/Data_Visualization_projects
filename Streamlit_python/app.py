import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.title("Sentiment Analysis of Tweets About US Airlines")
st.sidebar.title("Sentiment Analysis of Tweets About US Airlines")

st.markdown("Sentiment Analysis Application✈️ ")
st.sidebar.markdown("Sentiment Analysis Application✈️ ")


data_url = ("/home/rhyme/Desktop/Project/Tweets.csv")


#if the app is re-run, to reduce the cpu cycles,we use cache
@st.cache(persist=True)
def load_data():
    data = pd.read_csv(data_url)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()

#to display the Tweets
#st.write(data)
st.sidebar.subheader("Random Tweets")
random_tweet = st.sidebar.radio('Sentiment',('positive','neutral','negative'))
st.sidebar.markdown(data.query('airline_sentiment==@random_tweet')[['text']].sample(n=1).iat[0,0])


st.sidebar.markdown("## Number of Tweets by Sentiment")
select = st.sidebar.selectbox('Type of Chart!',['histogram','pie-chart'], key=1)
sentiment_count = data['airline_sentiment'].value_counts()
#st.write(sentiment_count)
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})


if not st.sidebar.checkbox("Hide", True):
    st.markdown("## Number of tweets by sentiment")
    if select == 'histogram':
        fig = px.bar(sentiment_count,x='Sentiment',y='Tweets', color='Tweets',height=500)
        st.plotly_chart(fig)

    else:
        fig = px.pie(sentiment_count,values='Tweets',names='Sentiment')
        st.plotly_chart(fig)

st.sidebar.subheader("Time and Location of tweets")
hour = st.sidebar.slider("Hour of day",0,23)
modified_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox("Close", True, key=1):
    st.markdown("## tweets locations based on time of day")
    st.markdown("%i tweets between %i:00 and %i:00"%(len(modified_data),hour,(hour+1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show tweets:",False):
        st.write(modified_data['text'])

st.sidebar.subheader("Tweets by Airlines")
choice = st.sidebar.multiselect('Pick airlines',('US Airways','United','American','Southwest','Delta','Virgin America'), key=0)

if len(choice)>0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x='airline',y='airline_sentiment',histfunc='count',color='airline_sentiment',facet_col='airline_sentiment',labels={'airline_sentiment':'tweets'},height=800,width=600)
    st.plotly_chart(fig_choice)

st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Sentiment Word Cloud',('positive','neutral','negative'))
if not st.sidebar.checkbox("Close",True,key='3'):
    st.subheader("Word Cloud for %s sentiment"%(word_sentiment))
    df = data[data['airline_sentiment']==word_sentiment]
    words = ' '.join(df['text'])
    pro_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word!= 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white',height=640,width=640).generate(pro_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()
