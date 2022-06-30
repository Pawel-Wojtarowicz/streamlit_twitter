import tweepy
import json
import pandas as pd
import streamlit as st
import plotly.express as px


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
        screen_name=user, count=80, tweet_mode="extended")
    columns = ["User", "Tweet"]
    data = []

    for tweet in tweets:
        data.append(
            [tweet.user.screen_name, tweet.full_text])

    df = pd.DataFrame(data, columns=columns)
    return df


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
            st.write("Soon..")

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
                fig.update_layout(height=1000, width=500)

    with st.container():
        st.write("---")
        left_column, middle_column, right_column = st.columns(3)
        with left_column:
            pass
        with middle_column:
            if uploaded_file:
                st.plotly_chart(fig)
                pass
        with right_column:
            text_area = st.text_area("input:")
            print(type(text_area))
            print(text_area)


if __name__ == '__main__':
    credentials = 'credentials.json'
    api = authentication(credentials)
    main()
