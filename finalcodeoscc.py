# -*- coding: utf-8 -*-
"""FinalCodeOSCC.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17TqflhXYaDb-QUdLxbgasnTPOqm6zbp6
"""

!pip install pyspark

!pip install vaderSentiment
!pip install transformers

!pip install tweepy

!pip install findspark

import tweepy
# import csv
# import time
# import os
from tweepy import OAuthHandler
from tweepy import Stream
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

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

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
# stream_tweet = Listener(consumer_key, consumer_secret, access_token, access_token_secret)

stream = Stream(auth,listener=Listener)
stream.filter(track=keywords)

# stream by keywords
keywords = ['Bitcoin', 'Ethereum', 'Btn', 'Eth']

# stream_tweet.filter(track=keywords)



stream_tweet = Listener(consumer_key, consumer_secret, access_token, access_token_secret)

# stream by keywords
keywords = ['Bitcoin', 'Ethereum', 'Btn', 'Eth']

stream_tweet.filter(track=keywords)

classifier = pipeline("sentiment-analysis")
analyzer = SentimentIntensityAnalyzer()

import findspark

# initialize your spark directory
# findspark.init('/home/nilabja/spark-2.3.1-bin-hadoop2.7')


from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import *
import re
import time
from textblob import TextBlob
from collections import namedtuple
import datetime


# Creating the Spark Context
sc = SparkContext(master="local[2]", appName="TwitterSentiment")
sc.setLogLevel("ERROR")

#creating the streaming context
ssc = StreamingContext(sc, 10)
# ssc.checkpoint("checkpoint")

#creating the SQL context
sqlContext = SQLContext(sc)


# lines = ssc.socketTextStream("localhost", 5599)

#Function to clean tweet
def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", str(tweet)).split())


#Polarity analysis of a tweet
def analyze_sentiment_polarity(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    return analysis.sentiment.polarity

#subjectivity analysis of a tweet
def analyze_sentiment_subjectivity(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    return str(analysis.sentiment.subjectivity)

classifier = pipeline("sentiment-analysis")
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment_pos(tweet):
    sentiment_dict = analyzer.polarity_scores(tweet)
    return sentiment_dict['pos']

def analyze_sentiment_Neg(tweet):
    sentiment_dict = analyzer.polarity_scores(tweet)
    return sentiment_dict['neg']

def analyze_sentiment_Neu(tweet):
    sentiment_dict = analyzer.polarity_scores(tweet)
    return sentiment_dict['neu']

def analyze_sentiment_Comp(tweet):
    sentiment_dict = analyzer.polarity_scores(tweet)
    return sentiment_dict['compound']

def analyze_sentiment_BERT_int(tweet):
    sentiment_dict = classifier(tweet)
    return sentiment_dict['label']

def analyze_sentiment_BERT(tweet):
    sentiment_dict = classifier(tweet)
    return sentiment_dict['score']

a =  analyze_sentiment_Comp("die")
a

lines = ["Bitcoin will crash","Use your ethereum","Hello World","Bitcoin is the best","this news is disapointing"]
tweet = sc.parallelize(lines)

# #Transforming using basic spark functions
sentiment = tweet.map(lambda text: (text, analyze_sentiment_polarity(text),
                                    analyze_sentiment_subjectivity(text),
                                    analyze_sentiment_pos(text),
                                    analyze_sentiment_Neg(text),
                                    analyze_sentiment_Neu(text),
                                    analyze_sentiment_Comp(text),
                                    ))
# words = lines.flatMap(lambda text: text.split(" ")).filter(lambda text: text.lower().startswith('#'))

sentiment = tweet.map(lambda text: (text, analyze_sentiment_polarity(text), analyze_sentiment_subjectivity(text)))

print(sentiment.collect())

sent2 = tweet.map(lambda text: (text, analyze_sentiment_polarity(text),
                                    analyze_sentiment_subjectivity(text),
                                    analyze_sentiment_pos(text),
                                    analyze_sentiment_Neg(text),
                                    analyze_sentiment_Neu(text),
                                    analyze_sentiment_Comp(text),
                                    ))

print(sent2.collect())

fields = ("hashtags", "count")
Tagscount = namedtuple('Tagscount', fields)

sentimentfields = ("text", "polarity", "subjectivity")
Sentimentobject = namedtuple('Sentimentobject', sentimentfields)

sentiment.window(180, 60).map(lambda p: Sentimentobject(p[0], p[1], p[2])).foreachRDD(
    lambda rdd: rdd.toDF().registerTempTable("sentiment"))
words.countByValueAndWindow(180, 60).map(lambda p: Tagscount(p[0], p[1])).foreachRDD(
    lambda rdd: rdd.toDF().sort(desc('count')).limit(10).registerTempTable("hashtags"))

response = input("Do you want to start the twitter stream ? Y/N (Please execute your stream listener in another terminal session and then put Y)\n")

if response == "Y":
    ssc.start()
    print("Session Started.....")
    print("Collecting tweets...waiting for 60 seconds..")

    time.sleep(60)
    print("Tweets Collected....")
    ssc.awaitTermination()

else:
    print("You ended the program")
    exit()

count = 0
    while count < 10: #We will run the loop 10 times for demonstration
        print("Waiting for 30 Seconds.....")
        time.sleep(30) #This loop will run every 30 seconds. The time interval can be increased as per your wish
        top_10_tweets = sqlContext.sql('Select * from hashtags')
        top_10_df = top_10_tweets.toPandas()

        print("------------------------------- \n")
        print(top_10_df)

        pos_sentiment = sqlContext.sql('Select count(text) from sentiment where polarity = 1')
        neu_sentiment = sqlContext.sql('Select count(text) from sentiment where polarity = 0')
        neg_sentiment = sqlContext.sql('Select count(text) from sentiment where polarity = -1')

        pos_df = pos_sentiment.toPandas()
        neu_df = neu_sentiment.toPandas()
        neg_df = neg_sentiment.toPandas()

        totalsentiment = pos_df['count(text)'].iloc[0] + neg_df['count(text)'].iloc[0] + neu_df['count(text)'].iloc[0]

        percent_pos = (pos_df['count(text)'].iloc[0] / totalsentiment) * 100
        print('Percentage of Positive Sentiment = {} %'.format(round(percent_pos, 2)))

        percent_neu = (neu_df['count(text)'].iloc[0] / totalsentiment) * 100
        print('Percentage of Neutral Sentiment = {} %'.format(round(percent_neu, 2)))

        percent_neg = (neg_df['count(text)'].iloc[0] / totalsentiment) * 100
        print('Percentage of Negative Sentiment = {} %'.format(round(percent_neg, 2)))

        count = count + 1
        #Updating latest hashtag count in a S3 bucket file
        csv_buffer = StringIO()
        top_10_df.to_csv(csv_buffer)

        ts = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
        filename = str("hashtags_" +  ts + ".csv")

