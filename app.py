import tweepy
import json
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go


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
    columns = ["Time", "User", "Tweet"]
    data = []

    for tweet in tweets:
        data.append([tweet.created_at, tweet.user.screen_name, tweet.text])

    df = pd.DataFrame(data, columns=columns)
    df.to_csv("tweety.csv")


def create_csv_from_user_tweets(user):
    tweets = api.user_timeline(
        screen_name=user, count=200, tweet_mode="extended")
    columns = ["Time", "User", "Tweet"]
    data = []

    for tweet in tweets:
        data.append(
            [tweet.created_at, tweet.user.screen_name, tweet.full_text])

    df = pd.DataFrame(data, columns=columns)
    return df
    # df.to_csv("tweety.csv")


def user_tweets(user):
    tweets = api.user_timeline(
        screen_name=user, count=200, tweet_mode="extended")
    for tweet in tweets:
        print(tweet.created_at, tweet.full_text)


@st.cache
def convert_df(df):
    # Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def main():
    #### STREAMLIT ####
    st.set_page_config(page_title="My Website",
                       page_icon=":bar_chart:", layout="wide")
    st.title("Streamlit with Twitter")

    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.subheader("Save tweets to the file.")
            user_input_csv = st.text_input(
                "Provide Twitter ID:", key="csv")

            csv = convert_df(create_csv_from_user_tweets(user_input_csv))
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='data.csv',
                mime='text/csv',
            )

        with right_column:
            st.subheader("Save tweets to DB.")
            st.write("Soon...")

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
                # fig = pd.DataFrame(df.groupby('User').count(), columns=['Tweets'])
                fig = px.bar(df, x="User", color="User")
                fig.update_xaxes(title="")
                fig.update_yaxes(title="Number of Tweets")

    with st.container():
        st.write("---")
        left_column, middle_column, right_column = st.columns(3)
        with left_column:
            pass
        with middle_column:
            if uploaded_file:
                # st.bar_chart(fig, width=1500, height=500) 
                st.plotly_chart(fig, width=1500, height=500) 
        with right_column:
            pass


if __name__ == '__main__':
    credentials = 'credentials.json'
    api = authentication(credentials)
    main()
