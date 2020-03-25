# coding=utf8

'''
version: March 25, 2020 02:50 PM
Last revision: March 25, 2020 02:55 PM

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
    client = MongoClient('mongodb://' + dbip + ':' + str(dbport), serverSelectionTimeoutMS = 3000)
except errors.ServerSelectionTimeoutError as err:
    client = None
    print("pymongo ERROR:", err)

db = client[dbName]

'''
add chat status
'''
def add_status():
    collectionName = 'chatStatus'
    cdccollection = db[collectionName]
    document = cdccollection.find_one({'_id': ObjectId(id)})
    CDCnewsDto.CDCnewsDto.id = document.get('_id')
    CDCnewsDto.CDCnewsDto.body = document.get('body')
    return CDCnewsDto


'''
delete status
'''
