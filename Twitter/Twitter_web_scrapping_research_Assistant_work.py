from calendar import week
from http import client
import re
from importlib_metadata import metadata
import tweepy
import acad_research
import pandas as pd
from re import search

# read token
client = tweepy.Client(bearer_token=acad_research.BEARER_TOKEN, wait_on_rate_limit=True)

#query='purchase (coronavirus OR covid19) -is:retweet lang:en'
#query='household (amazon OR flipkart) -is:retweet lang:en place:India has:geo'
#query='shopping (sale) -is:retweet lang:en place:India has:geo'
#query='#BigBillionDay (#GreatIndiaFestival) -is:retweet lang:en'
query='purchase (BigBillionDay OR GreatIndiaFestival) -is:retweet lang:en'
tweets=[]

#----------------------------------------------------Debugging code block ------------------------------------#
''''
start_time = '2021-03-06T00:00:00Z'
#end_time = '2021-05-02T00:00:00Z'
response = client.search_all_tweets(query=query, max_results=500, start_time=start_time)
for tweet in response.data:
    tweets.append(tweet.text)
'''
#--------------------------------------------------------------------------------------------------------------#

''''
# Get Tweet counts day basis 
response = client.get_all_tweets_count(query=query, start_time=start_time, end_time=end_time, granularity='day')
for tweet in response.data:
    print(tweet)
'''    

#for tweet in tweepy.Paginator(client.search_all_tweets, query=query, max_results=100, start_time=start_time, end_time=end_time).flatten(limit=450):
#    tweets.append(tweet.text)

#next_token=metadata.get("next_token")
#response = client.search_all_tweets(query=query, pagination_token=next_token ,max_results=5000, start_time=start_time, end_time=end_time, tweet_fields=['created_at'])



#for i in range(0,10):
#    response = client.search_all_tweets(query=query, max_results=500, start_time=start_time, end_time=end_time, tweet_fields=['created_at'])
#    for tweet in response.data:
#        #print(tweet.text)
#        tweets.append(tweet.text)
#    i+=1

 
tmp=[]
for i in range(30,0,-1):
    if (len(str(i)))==1:
        i='0'+str(i)
    else:
        pass
    start_time = '2021-05-01T00:00:00Z'
    end_time = '2021-09-'+str(i)+'T00:00:00Z'
    
    #end_time = '2021-05-02T00:00:00Z'
    response = client.search_all_tweets(query=query, max_results=500, start_time=start_time, end_time=end_time, tweet_fields=['created_at'])
    #response = client.search_all_tweets(query=query, max_results=500, start_time=start_time)
    #response = client.search_all_tweets(query=query, max_results=500, start_time='2021-03-04T00:00:00Z',end_time = '2021-04-30T00:00:00Z')
    
    if not response.data:
        print("No data found for this iteration")
        continue
    else:
        print(end_time)
        pass

    for tweet in response.data:
        tweets.append(tweet.text)
    #break

#tweets = [tweet.full_text for tweet in response.data]
tweets_df = pd.DataFrame(tweets, columns=['Tweets'])

# Data cleaning using regular expression 
for _, row in tweets_df.iterrows():
    row['Tweets'] = re.sub('http\S+', '', row['Tweets'])
    row['Tweets'] = re.sub('#\S+', '', row['Tweets'])
    row['Tweets'] = re.sub('@\S+', '', row['Tweets'])
    row['Tweets'] = re.sub('\\n', '', row['Tweets'])

tweets_df = tweets_df[~tweets_df['Tweets'].str.contains("RT")]
#tweets_df.drop_duplicates(keep='first', inplace=True)
print(tweets_df.shape)
tweets_df.reset_index(drop=True)
tweets_df.to_csv('tweets_purchase_bearer_18_05_household.csv',mode='a',index=False)
