import app
import up_to_atlas as uta

if __name__ == '__main__':
    data = app.search_twitter_query('life')
    tweets_df, authors_df = app.process_response(data)
    uta.pandas_to_atlas(tweets_df, authors_df)
