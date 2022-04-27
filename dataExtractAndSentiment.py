import tweepy
# import csv
# import time
# import os
import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
# from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
# from vaderSentiment import sentiment as vaderSentiment


consumer_key = 'Iee8qgYaRZpAQjKn4138goQqT'
consumer_secret='wO5GSrRHioFnMPJGgJlnhTAApBIUniPzNyBxUkZKxBit2Ablyt'

access_token='1509487966238158855-2RzmwozwZv8SdIEXkEFKik2QRXJfz9'
access_token_secret='45d1lSqc0PQBuIQntvvl2XPcIFAByUrELXhd9ZrSK9i0v'

auth = tweepy.OAuthHandler((consumer_key), consumer_secret)

auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

tweetList = []

bannedWords = ['nft', 'giveaway', 'referral']

class Listener(tweepy.Stream):

    tweets = []
    limit = 1000
    def on_status(self, status):
        self.tweets.append(status)
        if(status.user.followers_count > 100) and not any(word in status.text.lower().split(" ") for word in bannedWords):
            
            print(status.user.screen_name + ":" + status.text)
            tweetList.append(status.text)


        if(len(tweetList)==self.limit):
            self.disconnect()


stream_tweet = Listener(consumer_key, consumer_secret, access_token, access_token_secret)

# stream by keywords
keywords = ['Bitcoin', 'Ethereum', 'Btn', 'Eth']

stream_tweet.filter(track=keywords)

classifier = pipeline("sentiment-analysis")
analyzer = SentimentIntensityAnalyzer()
# analyzer.polarity_scores()

# values from transformers
label = []
score = []
# values from vader sentiment
neg_val = []
pos_val = []
neu_val = []
comp_val = []

for j in tweetList:
    label.append([item["label"] for item in classifier(j)])
    score.append([item["score"] for item in classifier(j)] )  
    
    neg_val.append(analyzer.polarity_scores(j)['neg'])
    pos_val.append(analyzer.polarity_scores(j)['pos'])
    neu_val.append(analyzer.polarity_scores(j)['neu'])
    comp_val.append(analyzer.polarity_scores(j)['compound'])

df = pd.DataFrame({ 'BERT_label' : label, 'BERT_score': score, 'neg_val': neg_val, 'pos_val': pos_val, 'neu_val' : neu_val,'comp_val': comp_val, 'text':tweetList})
print(df.head(10))

df.to_csv('data.csv')