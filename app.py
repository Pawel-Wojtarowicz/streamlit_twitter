from turtle import position
import tweepy
import json
import pandas as pd
import streamlit as st

def authentication(creds):

    credentials = read_creds(creds)
    api_key, api_secrets = credentials['api_key'], credentials['api_secrets']
    token, token_secrets = credentials['access_token'], credentials['access_secret']

    auth = tweepy.OAuthHandler(api_key, api_secrets)
    auth.set_access_token(token, token_secrets)

    return tweepy.API(auth)

def read_creds(filename):

    with open(filename) as f:
        credentials = json.load(f)
    return credentials

def create_csv_from_timeline():
    tweets = api.home_timeline()
    columns=["Time", "User", "Tweet"]
    data = []
    
    for tweet in tweets:
        data.append([tweet.created_at, tweet.user.screen_name, tweet.text])
    
    df = pd.DataFrame(data, columns=columns)
    df.to_csv("tweety.csv")

def create_csv_from_user_tweets(user):
    tweets = api.user_timeline(screen_name=user, count=200, tweet_mode="extended")
    columns=["Time", "User", "Tweet"]
    data = []
    
    for tweet in tweets:
        data.append([tweet.created_at, tweet.user.screen_name, tweet.full_text])
    
    df = pd.DataFrame(data, columns=columns)
    df.to_csv("tweety.csv")

def user_tweets(user):
    tweets = api.user_timeline(screen_name=user, count=200, tweet_mode="extended")
    for tweet in tweets:
        print(tweet.created_at, tweet.full_text)

#### STREAMLIT ####
st.set_page_config(page_title="My Website", page_icon=":bar_chart:", layout="wide")
st.title("Streamlit with Twitter")

with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("Save tweets to CSV file.")
        st.write("Provide Twitter ID:")
    with right_column:
        st.subheader("Save tweets to DB.")
        st.write("Provide Twitter ID:")

with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.write("plot your data") 
        uploaded_file = st.file_uploader("Choose a CSV file.", type="csv")
    with right_column:
        if uploaded_file:
            df = pd.read_csv(uploaded_file, encoding="utf-8")
            st.dataframe(df[['User','Tweet']])
    st.write("---")
        
if __name__ == '__main__':
    credentials = 'credentials.json'
    api = authentication(credentials)
    #create_csv_from_user_tweets("pwojtarowicz1")
    #user_tweets("pwojtarowicz1")


    
