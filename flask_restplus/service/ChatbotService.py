# coding=utf8

'''
version: March 24, 2020 11:30 AM
Last revision: April 07, 2020 11:37 AM

Author : Chao-Hsuan Ke
'''

import requests

from model.DTO import CDCnewsDto
from service import DataService
from pymongo import MongoClient, errors
from bson.objectid import ObjectId
from unit import globals as golvar
from unit import connection as connvar

dbip = '10.136.154.5'
dbport = 8083
dbName = 'ncov2019'

'''
intent
'''
def get_IntentRequestId(userName, query):
    url = connvar.analyticsServicetUrl
    postQuery = {'userName': userName,
                 'type': 'analytic',
                 'query': query
                 }
    x = requests.get(url, postQuery)
    intentJSON = x.json()
    # print('responseId', intentJSON.get('responseId'))
    # print('tags', len(intentJSON.get('tags')))
    # print(intentJSON.get('tags'))
    # print(intentJSON.get('tags')[0].get('locations')[0])
    return intentJSON

'''
start
'''
def get_Response(userName, country, requestId, responseNum, query):
    data = {}
    data['userName'] = userName
    if requestId == 0:                  # cdc news
        responseItems = DataService.get_GovernmentDeclaration(responseNum)
        # for item in responseItems:
        #     print(item, responseItems[item])
        #print(requestId, response)
        data['type'] = golvar.govType
        if len(responseItems) > 0:
            data['statue'] = True
        else:
            data['statue'] = False
        Items = []
        for item in responseItems:
            Items.append(responseItems[item])
        data['items'] = Items
    elif requestId == 1:                  # Delta declaration
        responseItems = DataService.get_DeltaDeclaration(responseNum)
        data['type'] = golvar.deltaType
        if len(responseItems) > 0:
            data['statue'] = True
        else:
            data['statue'] = False
        Items = []
        for item in responseItems:
            Items.append(responseItems[item])
        data['items'] = Items
    elif requestId == 2:                    # China News
        responseItems = DataService.get_ChinaNews(responseNum)
        data['type'] = golvar.pubNewsType
        if len(responseItems) > 0:
            data['statue'] = True
        else:
            data['statue'] = False
        Items = []
        for item in responseItems:
            Items.append(responseItems[item])
        data['items'] = Items
    elif requestId == 3:                    # QA
        responseItems = DataService.get_QA(userName, query)
        Items = []
        for item in responseItems:
            Items.append(responseItems[item])
        data['items'] = Items
    elif requestId == 4:                    # Rumors
        responseItems = DataService.get_Rumors(userName, query)
        Items = []
        for item in responseItems:
            Items.append(responseItems[item])
        data['items'] = Items
    elif requestId == 5:                    # Epidemic Dashboard
        responseItems = DataService.get_EpidemicDashboard(userName, country)
        data['type'] = golvar.EpidemicType
        if len(responseItems) > 0:
            data['statue'] = True
        else:
            data['statue'] = False
        Items = []
        for item in responseItems:
            Items.append(responseItems[item])
        data['items'] = Items
    elif requestId == 6:                # Travel Alert
        responseItems = DataService.get_TravelAlert(userName, country)
        data['type'] = golvar.TravelAlertType
        if len(responseItems) > 0:
            data['statue'] = True
        else:
            data['statue'] = False
        Items = []
        for item in responseItems:
            Items.append(responseItems[item])
        data['items'] = Items
    #elif requestId == 7:                # Self Test
    elif requestId == 8:                # Google News
        responseItems = DataService.get_GoogleNews(country, responseNum)
        Items = []
        for item in responseItems:
            Items.append(responseItems[item])
        if len(Items) > 0:
            data['status'] = True
            data['items'] = Items
        else:
            data['items'] = None


    return data






'''
db connection 
'''
# try:
#     # try to instantiate a client instance
#     client = MongoClient('mongodb://' + dbip + ':' + str(dbport), serverSelectionTimeoutMS = 3000)
# except errors.ServerSelectionTimeoutError as err:
#     client = None
#     print("pymongo ERROR:", err)
#
# db = client[dbName]

'''
CDC
query CDC news
'''
# def get_CDC_new(id):
#     collectionName = 'news_cdc'
#     cdccollection = db[collectionName]
#     document = cdccollection.find_one({'_id': ObjectId(id)})
#     CDCnewsDto.CDCnewsDto.id = document.get('_id')
#     CDCnewsDto.CDCnewsDto.body = document.get('body')
#     return CDCnewsDto


