# coding=utf8

'''
version: March 24, 2020 11:30 AM
Last revision: March 24, 2020 04:49 PM

Author : Chao-Hsuan Ke
'''

from model.DTO import CDCnewsDto
from pymongo import MongoClient, errors
from bson.objectid import ObjectId

dbip = '10.136.154.5'
dbport = 8083
dbName = 'ncov2019'

'''
db connection 
'''
try:
    # try to instantiate a client instance
    client = MongoClient('mongodb://' + dbip + ':' + str(dbport), serverSelectionTimeoutMS = 3000)
except errors.ServerSelectionTimeoutError as err:
    client = None
    print("pymongo ERROR:", err)

db = client[dbName]


def get_CDC_new(id):
    collectionName = 'news_cdc'
    cdccollection = db[collectionName]
    document = cdccollection.find_one({'_id': ObjectId(id)})
    CDCnewsDto.CDCnewsDto.id = document.get('_id')
    CDCnewsDto.CDCnewsDto.body = document.get('body')
    return CDCnewsDto

