import os
from pymongo import MongoClient
from dotenv import (load_dotenv, find_dotenv)

# find and load environment keys
load_dotenv(find_dotenv())
user = os.getenv('uname')
passwd = os.getenv('passwd')
host = os.getenv('hname')

# set the connection key to connect to atlas
connection_string = "mongodb+srv://{}:{}@{}/".format(user, passwd, host)

mongo_client = MongoClient(connection_string)

# get the database and the collection
db = mongo_client['tweetsdb']
collection = db['tweet_data']


def pandas_to_atlas(df1, df2):
    """
    a function to convert and upload pandas Dataframe to mongo atlas
    """
    df1.reset_index(inplace=True)
    df2.reset_index(inplace=True)
    if collection.insert_many(df1.to_dict('records')) and collection.insert_many(df2.to_dict('records')):
        print('Upload to atlas Successfully')
    else:
        print('Error whiles uploading to atlas')
