# coding=utf8

'''
version: March 30, 2020 10:00 AM
Last revision: March 31, 2020 01:10 PM

Author : Chao-Hsuan Ke
'''

import pymongo
import requests

from pymongo import MongoClient, errors
from model.DTO import ChinaNewsDto, DeltaDeclarationDTO, GovernmentDeclarationDTO, GoogleNewsDTO
from unit import globals as golvar


dbip = '10.136.154.5'
dbport = 8083
dbName = 'ncov2019'

'''
db connection 
'''
try:
    client = MongoClient('mongodb://' + dbip + ':' + str(dbport), serverSelectionTimeoutMS = 3000)
except errors.ServerSelectionTimeoutError as err:
    client = None
    print("pymongo ERROR:", err)

db = client[dbName]

'''
China/news
'''
def get_ChinaNews(country, responseNum):
    collectionName = golvar.collection_news
    statuscollection = db[collectionName]
    #document = statuscollection.find_one({'country': country.strip()})
    document = statuscollection.find({'country': country.strip()}).sort('timestamp', pymongo.DESCENDING)
    if document.count() < responseNum:
        responseNum = document.count()

    count = 0
    items = {}
    for DOC in document:
        if count < responseNum:
            jsonitems = {}
            responseItem = ChinaNewsDto
            jsonitems['id'] = DOC.get('_id')
            jsonitems['rank'] = (count+1)
            jsonitems['type'] = DOC.get('type')
            jsonitems['title'] = DOC.get('title')
            jsonitems['body'] = DOC.get('body')
            jsonitems['infoSource'] = DOC.get('infoSource')
            jsonitems['sourceUrl'] = DOC.get('sourceUrl')
            jsonitems['pubDate'] = str(DOC.get('pubDate'))
            jsonitems['continent'] = DOC.get('continent')
            jsonitems['country'] = DOC.get('country')
            jsonitems['timestamp'] = str(DOC.get('timestamp'))
            items[count] = jsonitems
            count += 1

    return items

'''
Delta Declaration
'''
def get_DeltaDeclaration(country, responseNum):
    collectionName = golvar.collection_deltadeclaration
    statuscollection = db[collectionName]
    document = statuscollection.find({'country': country.strip()}).sort('timestamp', pymongo.DESCENDING)
    if document.count() < responseNum:
        responseNum = document.count()

    count = 0
    items = {}
    for DOC in document:
        if count < responseNum:
            jsonitems = {}
            responseItem = DeltaDeclarationDTO
            jsonitems['id'] = str(DOC.get('_id'))
            jsonitems['rank'] = (count+1)
            jsonitems['type'] = DOC.get('type')
            jsonitems['title'] = DOC.get('title')
            jsonitems['body'] = DOC.get('body')
            jsonitems['infoSource'] = DOC.get('infoSource')
            jsonitems['sourceUrl'] = DOC.get('sourceUrl')
            jsonitems['pubDate'] = str(DOC.get('pubDate'))
            jsonitems['tag'] = DOC.get('tag')
            jsonitems['continent'] = DOC.get('continent')
            jsonitems['country'] = DOC.get('country')
            jsonitems['city'] = DOC.get('city')
            jsonitems['timestamp'] = str(DOC.get('timestamp'))
            items[count] = jsonitems
            count += 1
    return items

'''
Government Declaration
'''
def get_GovernmentDeclaration(country, responseNum):
    collectionName = golvar.collection_governmentdeclaration
    statuscollection = db[collectionName]
    document = statuscollection.find({'country': country.strip()}).sort('timestamp', pymongo.DESCENDING)
    if document.count() < responseNum:
        responseNum = document.count()

    count = 0
    items = {}
    for DOC in document:
        if count < responseNum:
            jsonitems = {}
            jsonitems['id'] = str(DOC.get('_id'))
            jsonitems['rank'] = (count+1)
            jsonitems['type'] = DOC.get('type')
            jsonitems['title'] = DOC.get('title')
            jsonitems['body'] = DOC.get('body')
            jsonitems['infoSource'] = DOC.get('infoSource')
            jsonitems['sourceUrl'] = DOC.get('sourceUrl')
            jsonitems['pubDate'] = str(DOC.get('pubDate'))
            jsonitems['continent'] = DOC.get('continent')
            jsonitems['country'] = DOC.get('country')
            jsonitems['city'] = DOC.get('city')
            jsonitems['timestamp'] = str(DOC.get('timestamp'))
            items[count] = jsonitems
            count += 1
    return items

'''
Google News
'''
def get_GoogleNews(country, responseNum):
    url = 'http://newsapi.org/v2/top-headlines'
    postQuery = {'country': country,
                 'category': golvar.category,
                 'apiKey': golvar.apiKey
                 }
    x = requests.get(url, postQuery)
    googlejson = x.json()
    # print(googlejson)
    # print(googlejson['status'])
    # print(googlejson['totalResults'])
    # print(len(googlejson['articles']))

    if len(googlejson['articles']) < responseNum:
        responseNum = len(googlejson['articles'])

    count = 0
    items = {}
    for DOC in googlejson['articles']:
        if count < responseNum:
            jsonitems = {}
            jsonitems['rank'] = (count + 1)
            jsonitems['title'] = DOC.get('title')
            jsonitems['body'] = DOC.get('description')
            jsonitems['infoSource'] = DOC.get('author')
            jsonitems['sourceUrl'] = DOC.get('url')
            jsonitems['pubDate'] = DOC.get('publishedAt')
            items[count] = jsonitems
            count += 1
    return items


