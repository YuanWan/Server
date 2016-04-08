import json

import newspaper
from newspaper import Article
import pymongo
from pymongo import MongoClient
import datetime
import sentiment_score


MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'news'
COLLECTION_NAME = "spacex"
connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
collection = connection[DBS_NAME][COLLECTION_NAME]


def insert_article(news):
    if news.title is None:
        return
    if news.text is None:
        return
    if news.authors is None:
        news.authors = "Not Available"
    if news.publish_date is None:
        news.publish_date = "Not Available"

    sentiments=sentiment_score.quick_score(news.text)

    news_object={
        "title":news.title,
        "text":news.text,
        "authors":news.authors,
        "publish_date":news.publish_date,
        "keywords":news.meta_keywords,
        "url":news.url,
        "source":news.source_url,
        "link_hash":news.link_hash,
        "image":news.top_image,
        "sentiments":sentiments
    }
    try:
        collection.insert_one(news_object)
    except:
        print("duplicated item")




import newspaper
#cnn_paper = newspaper.build('https://news.search.yahoo.com/search;_ylt=AwrSbg8sU59WVTwA3FJXNyoA;_ylu=X3oDMTB0NjZjZzZhBGNvbG8DZ3ExBHBvcwMxBHZ0aWQDBHNlYwNwaXZz?p=spacex&fr=uh3_magtech_web_gs&fr2=piv-web'
                            # , memoize_articles=True)
cnn_paper = newspaper.build('http://www.bing.com/news/search?q=spacex&go=Submit&qs=n&form=QBLH&scope=news&pq=spacex&sc=8-6&sp=-1&sk=&cvid=41BAF87FCCE043A99A665BDDBB5F9111'
                            , memoize_articles=True)
for article in cnn_paper.articles:
    article.download()
    article.parse()
    if article.title is not None:
        if "SpaceX" in article.title:
            insert_article(article)
print(cnn_paper.size())