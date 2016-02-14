from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import pymongo
from pymongo import MongoClient
import newspaper


MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'twitters'
connection = MongoClient(MONGODB_HOST, MONGODB_PORT)


access_token = "3220384082-tbVafpAHKF2OMyv3m68cUa1xLfTmJ8Riz6bry6l"
access_token_secret = "Eb1LiineWIRngaOwju91tEV3cexAcJhvCoxW4dNJ5UQMu"
consumer_key = "Ghy8tbRezuJH0AtSL1qcPjqm8"
consumer_secret = "bURQpyYNU7ZbPbZVLiCagInnbM4yZvK9hAFlhToLoZ3XjOCqSy"


class StdOutListener(StreamListener):
    def on_data(self, data):
        d = json.loads(data)
        text=d.get("text")
        print(text)
        analyzer_pa = TextBlob(text)
        # analyzer_nb = TextBlob(text, analyzer=NaiveBayesAnalyzer())
        print(analyzer_pa.sentiment)
        # print(analyzer_nb.sentiment)
        return True
    def on_error(self, status):
        print(status)

l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)
stream_open = stream.filter(track=['The Hateful Eight'], async=True)