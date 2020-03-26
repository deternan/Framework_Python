# coding=utf8

'''
version: March 23, 2020 10:05 AM
Last revision: March 26, 2020 05:32 PM

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
from service import user_service, ChatbotService, StatusService
from bson.objectid import ObjectId
from unit import globals as golvar

from flasgger import Swagger, swag_from


app = Flask(__name__)
api_blueprint = Blueprint('api', 'api', url_prefix='/api')

api = Api(app, prefix="/v1", title="APIs", description="ChatBot APIs.")
ns = Namespace("Test", description="APIs test")
ns2 = Namespace("Query", description="Data query")
ns3 = Namespace("chatStatus", description="chat status")
ns4 = Namespace("request", description="request")
api.add_namespace(ns)
api.add_namespace(ns2)
api.add_namespace(ns3)
api.add_namespace(ns4)
app.register_blueprint(api_blueprint)



class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


'''
User query testing
'''


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
CDC news
'''

@ns2.route('/db/query/newsCDC/<string:id>')
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
status
'''
@ns3.route('/add/<string:name>/<string:typeStr>/<int:requestId>/<int:count>', methods=['POST'])
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

@ns3.route('/query/<string:name>', methods=['GET'])
class statusQueery(Resource):
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

@ns3.route('/delete/<string:name>', methods=['GET'])
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
API request
'''

'''
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
        print(golvar.GlobalVar, golvar.RumorsType)
        #print('rumors type', golvar.APIlVar.RumorsType)
        #data['type'] = golvar.GlobalVar.RumorsType
        data['type'] = 'rumors'
        data['query'] = query

        url = 'http://10.136.154.13:5568/analytics/ir?'
        postQuery = {'userName': name,
                     'type': 'rumors',
                     'query' : query
                     }
        print(postQuery)
        #x = requests.post(url, postQuery)
        x = requests.get(url, postQuery)
        print(x)
        #print(x.json())
        return x.json()


'''
Main
'''
if __name__ == '__main__':
    app.run(debug=True)
