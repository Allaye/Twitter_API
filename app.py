import json
import os
import requests
import pandas as pd
from dotenv import (load_dotenv, find_dotenv)
from datetime import datetime

# find and load the env file
load_dotenv(find_dotenv())

app_key = os.environ.get('api_key')
app_secret = os.getenv('api_key_secret')
bearer_token = os.getenv('bearer_token')


def search_twitter(url):
    """
    authenicating the app
    """
    headers = {"Authorization": f"Bearer {bearer_token} "}
    response_json = requests.request('GET', url, headers=headers)
    return response_json.json()


def search_twitter_query(searchword, payload_size=10):
    """
    constructing the search query
    """
    tag = '{} -is:retweet'.format(searchword)
    expand = 'expansions=author_id'
    tweet_data = 'tweet.fields=author_id,public_metrics,created_at,lang'
    local_data = 'place.fields=country,name'
    user_data = 'user.fields=description,location,name,public_metrics,username,verified'
    max_data = 'max_results={}'.format(payload_size)
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&{}&{}&{}&{}".format(tag, expand, max_data,
                                                                                          tweet_data, user_data,
                                                                                          local_data)
    # url = 'https://api.twitter.com/1.1/search/tweets.json?q=%23National ID&include_entities=true'
    data = search_twitter(url=url)
    return data
    # print(json.dumps(data, indent=4, sort_keys=True))


def process_response(data):
    """
    A function to extract relevant fields from the tweets data
    """
    (tweet, tweet_id, lang, time_stamp) = ([], [], [], [])
    (retweet, reply, likes, quote) = ([], [], [], [])
    (username, name, verified, description) = ([], [], [], [])
    (followers, following, tweets) = ([], [], [])
    tweet_data = dict()
    author_data = dict()
    for i in data['data']:
        tweet.append(i['text']), tweet_id.append(i['id']), lang.append(i['lang']), time_stamp.append(i['created_at'])
        retweet.append(i['public_metrics']['retweet_count']), reply.append(i['public_metrics']['reply_count']),
        likes.append(i['public_metrics']['like_count']), quote.append(i['public_metrics']['quote_count'])
        tweet_data.update({'tweet': tweet, 'tweet_id': tweet_id, 'language': lang, 'time&date': time_stamp,
                           'retweet': retweet, 'reply': reply, 'likes': likes, 'quotes': quote})
    for j in data['includes']['users']:
        name.append(j['name']), username.append(j['username']), verified.append(j['verified']), description.append(
            j['description'])
        followers.append(j['public_metrics']['followers_count']), following.append(
            j['public_metrics']['following_count']),
        tweets.append(j['public_metrics']['tweet_count'])
        author_data.update({'name': name, 'username': username, 'is_verified': verified, 'description': description,
                            'followers_count': followers, 'following_count': following, 'tweets_count': tweets})
    tweet_data_df = pd.DataFrame(tweet_data)
    author_data_df = pd.DataFrame(author_data)
    tweet_data_df.to_csv('./tweets_data/data.csv')
    tweet_data_df.to_csv(f'./tweets_data/{datetime.today().strftime("%Y-%m-%d %H-%M-%S")}.csv')
    author_data_df.to_csv(f'./tweets_data/{datetime.today().strftime("%Y-%m-%d %H-%M-%S")}.csv')

    return tweet_data_df, author_data_df
