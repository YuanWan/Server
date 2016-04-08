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
import sentiment_score
import math


MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'twitter'
COLLECTION_NAME = "election"
connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
collection = connection[DBS_NAME][COLLECTION_NAME]


access_token = "3220384082-tbVafpAHKF2OMyv3m68cUa1xLfTmJ8Riz6bry6l"
access_token_secret = "Eb1LiineWIRngaOwju91tEV3cexAcJhvCoxW4dNJ5UQMu"
consumer_key = "Ghy8tbRezuJH0AtSL1qcPjqm8"
consumer_secret = "bURQpyYNU7ZbPbZVLiCagInnbM4yZvK9hAFlhToLoZ3XjOCqSy"


class StdOutListener(StreamListener):
    def on_data(self, data):
        insert_article(data)
        # d = json.loads(data)
        # text=d.get("text")
        # print(text)
        # analyzer_pa = TextBlob(text)
        # # analyzer_nb = TextBlob(text, analyzer=NaiveBayesAnalyzer())
        # print(analyzer_pa.sentiment)
        # print(analyzer_nb.sentiment)
        return True
    def on_error(self, status):
        print(status)


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

l = StdOutListener()
stream = Stream(auth, l)
stream_open = stream.filter(track=['Donald Trump', 'Ted Cruz', 'Hillary Clinton', 'Bernie Sanders','John Kasich'], async=True)



def insert_article(data):
    Trump=0
    Clinton=1
    Sanders=2
    Cruz=3
    Bush=4
    Carson=5
    Kasich=6
    Rubio=7

    d = json.loads(data)
    if isinstance(d.get("text"), str):
        analyzer=TextBlob(d.get("text"))
        d['analyzer']=analyzer.sentiment
        score=analyzer.sentiment[0]*analyzer.sentiment[1]
        d['score']=score
        validator=0
        if "Trump" in d.get("text") or "Donald" in d.get("text"):
            candidate=Trump
            validator+=1
        if "Clinton" in d.get("text") or "Hillary" in d.get("text"):
            candidate=Clinton
            validator+=1
        if "Sanders" in d.get("text") or "Bernie" in d.get("text"):
            candidate=Sanders
            validator+=1
        if "Cruz" in d.get("text") or "Ted" in d.get("text"):
            candidate=Cruz
            validator+=1
        if "Jeb" in d.get("text") or "Bush" in d.get("text"):
            candidate=Bush
            validator+=1
        if "Ben" in d.get("text") or "Carson" in d.get("text"):
            candidate=Carson
            validator+=1
        if "Rubio" in d.get("text") or "Marco" in d.get("text"):
            candidate=Rubio
            validator+=1

        if score != 0 and validator==1:
            d['candidate']=candidate
            try:
                user=d.get("user")
                follower=user.get("followers_count",0)
                favorite_count=d.get("favorite_count",0)
                # if favorite_count is None:
                #     favorite_count=0
                impact_factor=(1+follower/100+favorite_count)
                impact=impact_factor*score
                if impact>0:
                    impact=math.log(impact+1,10)
                else:
                    impact=0-math.log(0-impact+1,10)
                d['impact']=impact
                collection.insert_one(d)
                print(d.get("text"))
                print(analyzer.sentiment)
                print(d.get("score"))
                print(d.get("impact"))
            except:
                print("insert failed")