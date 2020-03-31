# coding=utf8

'''
version: March 23, 2020 10:05 AM
Last revision: March 31, 2020 01:08 PM

Author : Chao-Hsuan Ke
'''

'''
Reference

https://www.lagou.com/lgeduarticle/34790.html
https://www.freecodecamp.org/news/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563/
https://www.twblogs.net/a/5c2861cfbd9eee16b3dbddf3
https://github.com/noirbizarre/flask-restplus/issues/772

'''

import os, sys
import datetime
import requests
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import json


from flask import Flask, request, Blueprint
from flask_restplus import Resource, Api, Namespace
from service import user_service, ChatbotService, StatusService, DataService
from model.DTO import ChinaNewsDto, DeltaDeclarationDTO, GovernmentDeclarationDTO, GoogleNewsDTO
from bson.objectid import ObjectId
from unit import globals as golvar

from flasgger import Swagger, swag_from


app = Flask(__name__)
api_blueprint = Blueprint('api', 'api', url_prefix='/api')

api = Api(app, prefix="/v1", title="APIs", description="ChatBot APIs.")
ns = Namespace("Test", description="APIs test")
ns2 = Namespace("chat", description="chat status")
ns3 = Namespace("db", description="chat status")

ns4 = Namespace("request", description="request")
ns5 = Namespace("Query", description="Data query")
api.add_namespace(ns)
api.add_namespace(ns2)
api.add_namespace(ns3)

api.add_namespace(ns4)
api.add_namespace(ns5)
app.register_blueprint(api_blueprint)



class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@ns.route('/query/test/user/<string:name>/<string:email>')
class UserQuery(Resource):
    @api.doc('Query a user')
    @api.doc(responses={
        200: 'ok',
        400: 'not found',
        500: 'something is error'
    }, params={
        'name': {'description': 'user name',  'default': 'myName', 'required': True},
        'email': {'description': 'data type',  'type': 'string', 'default': 'status', 'required': True}
    })
    def post(self, name, email):
        content = request.get_json(silent=True)
        print(content)

        data = {}
        data['email'] = email
        data['name'] = name
        print(data)
        # returnData = user_service.get_return_new_user(data)
        # print('id', returnData.UserDto.id)
        # print('items.user.name', returnData.UserDto.user.name)
        # print('items.user.email', returnData.UserDto.user.email)
        return data



'''
chat-status-api-controller 
status
'''
@ns2.route('/status/add/<string:name>/<string:typeStr>/<int:requestId>/<int:count>', methods=['POST'])
class statusInsert(Resource):
    @api.doc(responses={
        200: 'ok',
        400: 'not found',
        500: 'something is error'
    }, params={'name': {'description': 'user name', 'default': 'my Name', 'required': True},
               'typeStr': {'description': 'data type',  'type': 'string', 'required': True, 'default': 'status'},
               'requestId': {'description': 'requestId', 'default': 0},
               'count': {'description': 'count', 'default': 0}
    })
    def post(self, name, typeStr, requestId, count):
        data = {}
        data['userName'] = name
        data['typeStr'] = typeStr
        data['requestId'] = requestId
        data['count'] = count
        data['timestamp'] = datetime.datetime.utcnow()
        response = StatusService.add_status(data)
        return response

@ns2.route('/status/check/<string:name>', methods=['GET'])
class statusCheck(Resource):
    @api.doc(responses={
        200: 'ok',
        400: 'not found',
        500: 'something is error'
    }, params={'name': {'description': 'user name', 'default': 'my Name', 'required': True}
    })
    def get(self, name):
        data = StatusService.get_Status(name)
        responseData = {}
        responseData['id'] = str(data.statusDto.id)
        responseData['userName'] = data.statusDto.userName
        responseData['type'] = data.statusDto.type
        responseData['requestId'] = data.statusDto.requestId
        responseData['count'] = data.statusDto.count
        responseData['timestamp'] = str(data.statusDto.timestamp.utcnow())
        return responseData

@ns2.route('/status/delete/<string:name>', methods=['GET'])
class statusDelete(Resource):
    @api.doc(responses={
        200: 'ok',
        400: 'not found',
        500: 'something is error'
    }, params={'name': {'description': 'user name', 'default': 'my Name', 'required': True}
    })
    def get(self, name):
        response = StatusService.delete_Status(name)
        return response


'''
data-query-controller
'''
'''
POST /db/public/China/news
'''
@ns3.route('/public/China/news/<string:country>/<int:responseNum>', methods=['POST'])
class ChinaNews(Resource):
    @api.doc(responses={
        200: 'success',
        403: 'Forbidden',
        404: 'not found'
    }, params={'country': {'description': 'query country',  'type': 'string', 'required': True, 'default': '中國'},
               'responseNum': {'description': 'Num of response', 'default': 3}
    })
    def post(self, country, responseNum):
        data = {}
        data['type'] = golvar.pubNewsType
        responseItems = DataService.get_ChinaNews(country, responseNum)
        if len(responseItems) > 0:
            data['status'] = True
        else:
            data['status'] = False
        Items = []
        count = 0
        for item in responseItems:
            Item = responseItems[item]
            Item = ChinaNewsDto
            Items.append(responseItems[item])
            #print(count, item, responseItems[item])
            count += 1
        data['items'] = Items
        return data

'''
POST /db/delta/declaration
'''
@ns3.route('/delta/declaration/<string:country>/<int:responseNum>', methods=['POST'])
class deltadeclaration(Resource):
    @api.doc(responses={
        200: 'success',
        403: 'Forbidden',
        404: 'not found'
    }, params={'country': {'description': 'query country',  'type': 'string', 'required': True, 'default': '台灣'},
               'responseNum': {'description': 'Num of response', 'default': 3}
    })
    def post(self, country, responseNum):
        data = {}
        data['type'] = golvar.deltaType
        responseItems = DataService.get_DeltaDeclaration(country, responseNum)

        if len(responseItems) > 0:
            data['status'] = True
        else:
            data['status'] = False
        Items = []
        count = 0
        for item in responseItems:
            Item = responseItems[item]
            Item = DeltaDeclarationDTO
            Items.append(responseItems[item])
            count += 1
        data['items'] = Items
        return data

'''
POST /db/government/Taiwan/declaration  collection_governmentdeclaration
'''
@ns3.route('/government/Taiwan/declaration/<string:country>/<int:responseNum>', methods=['POST'])
class governmentdeclaration(Resource):
    @api.doc(responses={
        200: 'success',
        403: 'Forbidden',
        404: 'not found'
    }, params={'country': {'description': 'query country',  'type': 'string', 'required': True, 'default': '台灣'},
               'responseNum': {'description': 'Num of response', 'default': 3}
    })
    def post(self, country, responseNum):
        data = {}
        data['type'] = golvar.govType
        responseItems = DataService.get_GovernmentDeclaration(country, responseNum)

        if len(responseItems) > 0:
            data['status'] = True
        else:
            data['status'] = False
        Items = []
        count = 0
        for item in responseItems:
            Items.append(responseItems[item])
            count += 1
        data['items'] = Items
        return data

'''
API request
'''
'''
POST /api/rumors/
rumors API query
'''
@ns4.route('/rumors/<string:name>/<string:query>', methods=['POST'])
class queryRumors(Resource):
    @api.doc(responses={
        200: 'ok',
        400: 'not found',
        500: 'something is error'
    }, params={'name': {'description': 'user name', 'default': 'my Name', 'required': True},
               'query': {'description': 'query',  'type': 'string', 'required': True, 'default': '口罩可以重複使用嗎'}
    })
    def post(self, name, query):
        data = {}
        data['userName'] = name
        data['type'] = golvar.RumorsType
        data['query'] = query

        url = 'http://10.136.154.13:5568/analytics/ir?'
        postQuery = {'userName': name,
                     'type': golvar.RumorsType,
                     'query' : query
                     }
        print(postQuery)
        #x = requests.post(url, postQuery)
        x = requests.get(url, postQuery)
        #print(x)
        return x.json()

'''
POST /api/rumors/
rumors API query
'''
@ns5.route('/google/news/<string:country>/<int:responseNum>', methods=['POST'])
class getGoogleNews(Resource):
    @api.doc(responses={
        200: 'ok',
        400: 'not found',
        500: 'something is error'
    }, params={'country': {'description': 'country',  'type': 'string', 'required': True, 'default': 'tw'},
               'responseNum': {'description': 'Num of response', 'default': 3}
    })
    def post(self, country, responseNum):
        data = {}
        #data['userName'] = name
        #data['country'] = country
        data['type'] = golvar.GoogleNewsType
        responseItems = DataService.get_GoogleNews(country, responseNum)
        if len(responseItems) > 0:
            data['status'] = True
        else:
            data['status'] = False
        Items = []
        count = 0
        for item in responseItems:
            Items.append(responseItems[item])
            count += 1
        data['items'] = Items
        return data


'''
CDC news
'''
@ns5.route('/db/query/newsCDC/<string:id>')
class dbQuery(Resource):
    @api.doc(responses={
        200: 'ok',
        400: 'not found',
        500: 'something is error'
    }, params={
        'id': 'the task identifier'
    })
    def get(self, id):
        data = ChatbotService.get_CDC_new(id)
        ## transfer to JSON
        responseData = {}
        responseData['id'] = str(data.CDCnewsDto.id)
        jsonstr = data.CDCnewsDto.body
        responseData['text'] = jsonstr
        return responseData



'''
GET and POST 
'''
@ns.route('/<int:id>/<string:name>')
class HelloWorld(Resource):
    @api.doc(responses={
        200: 'ok',
        400: 'not found',
        500: 'something is error'
    }, params={
        'id': 'the task identifier',
        'name': 'the user name'
    })
    def get(self, id):
        return {
            'status': 'you get a request.',
            'id': id
        }

    def post(self, id, name):
        return {
            'status': 'you post a request.',
            'id': id,
            'name': name
        }


'''
Main
'''
if __name__ == '__main__':
    app.run(debug=True)
