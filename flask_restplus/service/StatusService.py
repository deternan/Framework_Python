# coding=utf8

'''
version: March 25, 2020 02:50 PM
Last revision: April 01, 2020 05:12 PM

Author : Chao-Hsuan Ke
'''

import datetime

from pymongo import MongoClient, errors
from bson.objectid import ObjectId
from model.DTO import statusDto
#from unit import globals as golvar
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
query chat status
'''
def get_Status(userName):
    collectionName = connvar.collection_status
    statuscollection = db[collectionName]
    document = statuscollection.find_one({'userName': userName.strip()})

    if document is not None:
        jsonitems = {}
        jsonitems['id'] = str(document.get('_id'))
        jsonitems['userName'] = document.get('userName')
        jsonitems['requestId'] = document.get('requestId')
        jsonitems['type'] = document.get('type')
        jsonitems['count'] = document.get('count')
        jsonitems['timestamp'] = str(document.get('timestamp'))
        # statusDto.statusDto = None
        # statusDto.statusDto.id = str(document.get('_id'))
        # statusDto.statusDto.userName = document.get('userName')
        # statusDto.statusDto.requestId = document.get('requestId')
        # statusDto.statusDto.type = document.get('type')
        # statusDto.statusDto.count = document.get('count')
        # statusDto.statusDto.timestamp = str(document.get('timestamp'))
    else:
        #statusDto.statusDto = None
        jsonitems = None

    #return statusDto
    return jsonitems

'''
add chat status by userName
'''
def add_status(userName, requestId, type, count, repeatNotics, covid19Status):
    collectionName = connvar.collection_status
    statuscollection = db[collectionName]
    statuscollection.insert_one({
        'userName': userName,
        'requestId': requestId,
        'type': type,
        'count': count,
        'repeatNotics': repeatNotics,
        'covid19Status': covid19Status,
        'timestamp': datetime.datetime.utcnow()
    })
    return 'success'

'''
add chat status
'''
# def add_status(status):
#     collectionName = connvar.collection_status
#     statuscollection = db[collectionName]
#     statuscollection.insert_one(status)
#     return 'success'


'''
delete chat status
'''
def delete_Status(userName):
    collectionName = connvar.collection_status
    statuscollection = db[collectionName]
    document = statuscollection.delete_one({'userName': userName.strip()})
    return 'success'