import tweepy
# import csv
# import time
# import os
import pandas as pd

consumer_key = 'Iee8qgYaRZpAQjKn4138goQqT'
consumer_secret='wO5GSrRHioFnMPJGgJlnhTAApBIUniPzNyBxUkZKxBit2Ablyt'

access_token='1509487966238158855-2RzmwozwZv8SdIEXkEFKik2QRXJfz9'
access_token_secret='45d1lSqc0PQBuIQntvvl2XPcIFAByUrELXhd9ZrSK9i0v'

auth = tweepy.OAuthHandler((consumer_key), consumer_secret)

auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

bannedWords = ['nft', 'giveaway', 'referral']

class Listener(tweepy.Stream):

    # tweets = []
    # limit = 100
    def on_status(self, status):
        # self.tweets.append(status)
        if(status.user.followers_count > 100) and not any(word in status.text.lower().split(" ") for word in bannedWords):
            
            print(status.user.screen_name + ":" + status.text)

        # if(len(self.tweets)==self.limit):
        #     self.disconnect()


stream_tweet = Listener(consumer_key, consumer_secret, access_token, access_token_secret)

# stream by keywords
keywords = ['Bitcoin', 'Ethereum', 'Btn', 'Eth']

stream_tweet.filter(track=keywords)

