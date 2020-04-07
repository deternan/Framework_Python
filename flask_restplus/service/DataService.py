# coding=utf8

'''
version: March 30, 2020 10:00 AM
Last revision: April 06, 2020 03:07 PM

Author : Chao-Hsuan Ke
'''

import pymongo
import requests

from pymongo import MongoClient, errors
from unit import globals as golvar
from unit import connection as connvar

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
(Taiwan) Government Declaration
'''
def get_GovernmentDeclaration(responseNum):
    collectionName = connvar.collection_governmentdeclaration
    statuscollection = db[collectionName]
    #document = statuscollection.find({'country': country.strip()}).sort('timestamp', pymongo.DESCENDING)
    document = statuscollection.find({'country': '台灣'}).sort('timestamp', pymongo.DESCENDING)
    if document.count() < responseNum:
        responseNum = document.count()
    else:
        responseNum = golvar.responseNumLimit
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
Delta Declaration
'''
def get_DeltaDeclaration(responseNum):
    collectionName = connvar.collection_deltadeclaration
    statuscollection = db[collectionName]
    #document = statuscollection.find({'country': country.strip()}).sort('timestamp', pymongo.DESCENDING)
    document = statuscollection.find({'country': '台灣'}).sort('timestamp', pymongo.DESCENDING)
    if document.count() < responseNum:
        responseNum = document.count()
    else:
        responseNum = golvar.responseNumLimit
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
            jsonitems['tag'] = DOC.get('tag')
            jsonitems['continent'] = DOC.get('continent')
            jsonitems['country'] = DOC.get('country')
            jsonitems['city'] = DOC.get('city')
            jsonitems['timestamp'] = str(DOC.get('timestamp'))
            items[count] = jsonitems
            count += 1
    return items

'''
China/news
'''
def get_ChinaNews(responseNum):
    collectionName = connvar.collection_news
    statuscollection = db[collectionName]
    #document = statuscollection.find({'country': country.strip()}).sort('timestamp', pymongo.DESCENDING)
    document = statuscollection.find({'country': '中國'}).sort('timestamp', pymongo.DESCENDING)
    if document.count() < responseNum:
        responseNum = document.count()
    else:
        responseNum = golvar.responseNumLimit
    count = 0
    items = {}
    for DOC in document:
        if count < responseNum:
            jsonitems = {}
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
QA
'''
def get_QA(userName, query):
    url = connvar.IRserviceURL
    postQuery = {'userName': userName,
                 'type': 'qa',
                 'query': query
                 }
    x = requests.get(url, postQuery)
    QAjson = x.json()
    if len(QAjson.get('documents')) < golvar.responseNumLimit:
        responseNum = len(QAjson.get('documents'))
    else:
        responseNum = golvar.responseNumLimit
    count = 0
    items = {}
    for DOC in QAjson.get('documents'):
        if count < responseNum:
            jsonitems = {}
            jsonitems['id'] = DOC.get('_id')
            jsonitems['rank'] = (count + 1)
            jsonitems['title'] = DOC.get('title')
            jsonitems['body'] = DOC.get('body')
            jsonitems['infoSource'] = DOC.get('infoSource')
            jsonitems['sourceUrl'] = DOC.get('sourceUrl')
            jsonitems['pubDate'] = str(DOC.get('pubDate'))
            items[count] = jsonitems
            count += 1
    # return QAjson
    return items

'''
rumors
'''
def get_Rumors(userName, query):
    url = connvar.IRserviceURL
    postQuery = {'userName': userName,
                 'type': 'rumors',
                 'query': query
                 }
    x = requests.get(url, postQuery)
    rumorsjson = x.json()
    if len(rumorsjson.get('documents')) < golvar.responseNumLimit:
        responseNum = len(rumorsjson.get('documents'))
    else:
        responseNum = golvar.responseNumLimit
    count = 0
    items = {}
    for DOC in rumorsjson.get('documents'):
        if count < responseNum:
            jsonitems = {}
            jsonitems['id'] = DOC.get('_id')
            jsonitems['rank'] = (count + 1)
            jsonitems['title'] = DOC.get('title')
            jsonitems['body'] = DOC.get('body')
            jsonitems['infoSource'] = DOC.get('infoSource')
            jsonitems['sourceUrl'] = DOC.get('sourceUrl')
            jsonitems['pubDate'] = str(DOC.get('pubDate'))
            jsonitems['realness'] = DOC.get('realness')
            items[count] = jsonitems
            count += 1
    #return rumorsjson
    return items

'''
Epidemic Dashboard
'''
def get_EpidemicDashboard(userName, query):
    url = connvar.DBserviceURL
    postQuery = {'userName': userName,
                 'table_name': 'travel_alert',
                 'locations': query
                 }
    xE = requests.get(url, postQuery)
    Epidemicjson = xE.json()
    '''
    TravelAlert
    '''
    postQueryT = {'userName': userName,
                  'table_name': 'ncov_stats',
                  'locations': query
                  }
    xT = requests.get(url, postQueryT)
    travelalertjson = xT.json()

    items = {}
    jsonitems = {}
    DOCE = Epidemicjson.get('infos')[0]
    jsonitems['senderName'] = DOCE.get('senderName')
    jsonitems['headline'] = DOCE.get('headline')
    jsonitems['instruction'] = DOCE.get('instruction')
    jsonitems['severity_level'] = DOCE.get('severity_level')
    jsonitems['alert_disease'] = DOCE.get('alert_disease')
    jsonitems['areaDesc'] = DOCE.get('areaDesc')
    DOCT = travelalertjson.get('infos')[0]
    jsonitems['continentName'] = DOCT.get('continentName')
    jsonitems['countryName'] = DOCT.get('countryName')
    jsonitems['provinceName'] = DOCT.get('provinceName')
    jsonitems['currentConfirmedCount'] = DOCT.get('currentConfirmedCount')
    jsonitems['confirmedCount'] = DOCT.get('confirmedCount')
    jsonitems['suspectedCount'] = DOCT.get('suspectedCount')
    jsonitems['curedCount'] = DOCT.get('curedCount')
    jsonitems['deadCount'] = DOCT.get('deadCount')

    items[0] = jsonitems
    return items


'''
travel_alert
'''
def get_TravelAlert(userName, query):
    url = connvar.DBserviceURL
    '''
    TravelAlert
    '''
    postQueryT = {'userName': userName,
                 'table_name': 'ncov_stats',
                 'locations': query
                 }
    xT = requests.get(url, postQueryT)
    travelalertjson = xT.json()
    '''
    Epidemic Dashboard
    '''
    postQueryE = {'userName': userName,
                  'table_name': 'travel_alert',
                  'locations': query
                  }
    xE = requests.get(url, postQueryE)
    Epidemicjson = xE.json()

    items = {}
    jsonitems = {}
    DOCT = travelalertjson.get('infos')[0]
    jsonitems['continentName'] = DOCT.get('continentName')
    jsonitems['countryName'] = DOCT.get('countryName')
    jsonitems['provinceName'] = DOCT.get('provinceName')
    jsonitems['currentConfirmedCount'] = DOCT.get('currentConfirmedCount')
    jsonitems['confirmedCount'] = DOCT.get('confirmedCount')
    jsonitems['suspectedCount'] = DOCT.get('suspectedCount')
    jsonitems['curedCount'] = DOCT.get('curedCount')
    jsonitems['deadCount'] = DOCT.get('deadCount')
    DOCE = Epidemicjson.get('infos')[0]
    jsonitems['senderName'] = DOCE.get('senderName')
    jsonitems['headline'] = DOCE.get('headline')
    jsonitems['instruction'] = DOCE.get('instruction')
    jsonitems['severity_level'] = DOCE.get('severity_level')
    jsonitems['alert_disease'] = DOCE.get('alert_disease')
    jsonitems['areaDesc'] = DOCE.get('areaDesc')

    items[0] = jsonitems
    return items


'''
Google News
'''
def get_abbreviation(country):
    getAbb = None
    tagCheck = False
    if golvar.Taiwan_Chinese_dict.get(country) != None:
        getAbb = golvar.Taiwan_Chinese_dict.get(country)
        tagCheck = True

    if golvar.China_Chinese_dict.get(country) != None:
        getAbb = golvar.China_Chinese_dict(country)
        tagCheck = True

    if golvar.Japan_Chinese_dict.get(country) != None:
        getAbb = golvar.Japan_Chinese_dict.get(country)
        tagCheck = True

    if golvar.America_Chinese_dict.get(country) != None:
        getAbb = golvar.America_Chinese_dict.get(country)
        tagCheck = True


    if tagCheck == True:
        return getAbb
    else :
        return 'None'

def get_GoogleNews(countryStr, responseNum):
    country = get_abbreviation(countryStr)
    url = connvar.googleURL
    postQuery = {'country': country,
                 'category': connvar.category,
                 'apiKey': connvar.apiKey
                 }
    x = requests.get(url, postQuery)
    googlejson = x.json()

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


