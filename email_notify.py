import smtplib
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
import time
from threading import Timer


trend = 0
recipient = 'ywan003@e.ntu.edu.sg'
msg = 'Hello!'
user = 'datafryer@gmail.com'
pwd = ''
subject_positive = 'Trending: Positive'
body_positive = 'Your tracking tag is experiencing positive sentimental trend, congratulations'
subject_negative = 'Trending: Negative'
body_negative = 'Your tracking tag is experiencing negative sentimental trend, please check'
subject_v = 'Trending: Abnormal volume detected'
body_v = 'Your tracking tag is experiencing high volume of discussion, please check'

def send_email(user, pwd, recipient, subject, body):
    FROM = 'CyberPulse'
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % ("CyberPulse", ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(user, TO, message)
        server.close()
        print('successfully sent the mail')
    except:
        print("failed to send mail")


def load_t(data):
    global trend
    trend=trend+1

    d = json.loads(data)
    if isinstance(d.get("text"), str):
        analyzer = TextBlob(d.get("text"))
        d['analyzer'] = analyzer.sentiment
        score = analyzer.sentiment[0] * analyzer.sentiment[1]
        # d['score'] = score
        print(d.get("text"))
        print(score)
        if score<-0.4:
            send_email(user, pwd, recipient, subject_negative, body_negative)
        if score>0.4:
            send_email(user, pwd, recipient, subject_positive, body_positive)


def trending():
    global trend
    if trend>3:
        send_email(user, pwd, recipient, subject_v, body_v)
    trend=trend/3;


def times():
     time.sleep(180)
     trending()


access_token = "3220384082-fsBaRxEdiNhgQsTihGAESgUGNWEF6TKUq3oXJ2V"
access_token_secret = "k96u73rXHkZmjBUm8FTiPIsLY9awCDwOLfHz5Bzj92bKt"
consumer_key = "OhahezGH2pK6fHkGiBlO7JvzL"
consumer_secret = "bKqNRHKwEBEURGV7yKzoITWLXIigxUjSWydikV13ulM7AppoUa"


class StdOutListener(StreamListener):
    def on_data(self, data):
        load_t(data)
        return True

    def on_error(self, status):
        print(status)


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

l = StdOutListener()
stream = Stream(auth, l)
stream_open = stream.filter(track=['#Trump'],
                            async=True)


times()







