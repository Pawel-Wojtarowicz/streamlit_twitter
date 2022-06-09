import tweepy
import json
import pandas as pd

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

def user_tweets(user):
    tweets = api.user_timeline(screen_name=user, count=200, tweet_mode="extended")
    for tweet in tweets:
        print(tweet.created_at, tweet.full_text)

if __name__ == '__main__':
    credentials = 'credentials.json'
    api = authentication(credentials)
    # create_csv_from_timeline()
    user_tweets("pwojtarowicz1")

    
    
