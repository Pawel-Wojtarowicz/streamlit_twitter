from datetime import datetime
import tweepy
import json
import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_tags import st_tags
import snscrape.modules.twitter as sntwitter


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


def create_csv_from_user_tweets(users):

    columns = ["User", "Tweets"]
    data = []
    error = ""
    for user in users:
        try:
            tweets = api.user_timeline(
                screen_name=user, count=80, tweet_mode="extended")
            for tweet in tweets:
                data.append([tweet.user.screen_name, tweet.full_text])
        except:
            error += user + " "
            pass

    df = pd.DataFrame(data, columns=columns)
    return df, error


def create_csv_from_user_tweets_from_the_time_interval(provided_user_list, fromdate, todate):
    columns = ["User", "Tweets"]
    tweets = []

    for user in provided_user_list:
        query = f"(from:{user}) until:{todate} since:{fromdate}"
        for tweet in sntwitter.TwitterSearchScraper(query).get_items():
            tweets.append([tweet.user.username, tweet.content])
    df = pd.DataFrame(tweets, columns=columns)
    return df


@st.cache
def convert_df(df):
    # Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def main():
    st.set_page_config(page_title="My Website",
                       page_icon=":bar_chart:", layout="wide")
    st.title("Streamlit with Twitter")

    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            st.write("---")
            st.subheader("Save tweets to the file usinng Twitter scrapper")
            keywords_scrapper = st_tags(label="Enter Accounts from Twitter:",
                               text="Press enter to add more", value=["elonmusk", "barackobama"], key="scrapper")
        with right_column:
            st.write("---")
            st.subheader("Save tweets to the file using Twitter API")
            keywords_api = st_tags(label="Enter Accounts from Twitter:",
                               text="Press enter to add more", value=["trzaskowski_", "bweglarczyk"], key="api")
            
            csv_api= convert_df(create_csv_from_user_tweets(keywords_api)[0])

            if create_csv_from_user_tweets(keywords_api)[1]:
                st.write("User(s):", create_csv_from_user_tweets(
                    keywords_api)[1], "not found.")
            else:
                pass
        
    with st.container():
        today = datetime.today().date()
        # dates = []
        left_column, middle_column, right_column = st.columns([1, 1, 2])
        with left_column:
            # dates.append(st.date_input("From:", today))
            fromdate = st.date_input("From:", today)
        with middle_column:
            # dates.append(st.date_input("To:", today))
            todate = st.date_input("To:", today)
        
         
        st.download_button(
                label="Download data as CSV",
                data=csv_scrapper,
                file_name='data.csv',
                mime='text/csv',
                key="scrappper"
            )
        with right_column:
    
            st.download_button(
                label="Download data as CSV",
                data=csv_api,
                file_name='data.csv',
                mime='text/csv',
                key="api"
            )

    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.write("Plot your data.")
            uploaded_file = st.file_uploader("Choose a CSV file.", type="csv")
        with right_column:
            if uploaded_file:
                df = pd.read_csv(uploaded_file, encoding="utf-8")
                st.dataframe(df[['User', 'Tweets']])

                fig = df.groupby("User", as_index=False).count()
                fig = px.bar(fig, x="User", y="Tweets", color="User", title="Bar chart", labels={
                             "Tweets": "Number of Tweets", "User": "Users"})
                fig.update_layout(height=800, width=400)

    with st.container():
        st.write("---")
        left_column, middle_column, right_column = st.columns(3)
        with left_column:
            pass
        with middle_column:
            if uploaded_file:
                st.plotly_chart(fig)
        with right_column:
            pass


if __name__ == '__main__':
    credentials = 'credentials.json'
    api = authentication(credentials)
    main()
