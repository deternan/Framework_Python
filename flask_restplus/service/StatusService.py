# coding=utf8

'''
version: March 25, 2020 02:50 PM
Last revision: March 26, 2020 04:25 PM

Author : Chao-Hsuan Ke
'''

from pymongo import MongoClient, errors
from bson.objectid import ObjectId
from model.DTO import statusDto
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
query chat status
'''
def get_Status(userName):
    collectionName = golvar.collection_status
    statuscollection = db[collectionName]
    document = statuscollection.find_one({'userName': userName.strip()})
    statusDto.statusDto.id = document.get('_id')
    statusDto.statusDto.userName = document.get('userName')
    statusDto.statusDto.type = document.get('type')
    statusDto.statusDto.requestId = document.get('requestId')
    statusDto.statusDto.count = document.get('count')
    statusDto.statusDto.timestamp = document.get('timestamp')
    return statusDto

'''
add chat status
'''
def add_status(status):
    collectionName = golvar.collection_status
    statuscollection = db[collectionName]
    statuscollection.insert_one(status)
    return 'success'


'''
delete chat status
'''
def delete_Status(userName):
    collectionName = golvar.collection_status
    statuscollection = db[collectionName]
    document = statuscollection.delete_one({'userName': userName.strip()})
    return 'success'